from datetime import datetime
import sys
import psutil
import serial
import time
import math
import platform

if platform.system() == 'Windows':
    import wmi

arduino_port = 'COM11'  # change it to your /dev/ttyACM[port] or /dev/ttyUSB[port] for linux or COM[port] for windows
timeout_readings = 1  # fix this
timeout_send = 0.01
time_format = "%H:%M %d/%m/%Y"

amd_names = ['AMD', 'Advanced micro devices', 'Advanced Micro Devices, Inc.', 'Radeon']
nvidia_names = ['Nvidia']
intel_names = ['Intel Corporation', 'Intel']


class Main:

    def __init__(self) -> None:
        self.mem_stats = self.cpu_stats = self.cpu_stats_total = None
        self.cpu_count_real = psutil.cpu_count(False)
        self.cpu_count = psutil.cpu_count()
        self.connection = None
        self.is_amd_card = self.is_nvidia_card = self.is_intel_card = False

        self.startup_time = time.strftime(time_format, time.localtime(psutil.boot_time()))
        self.current_time = self.uptime = self.day = None
        self.sensors = self.cpu_fan = None
        self.gpu_devices = []

    @staticmethod
    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s%s" % (s, size_name[i])

    def get_stats(self):
        self.cpu_stats = ""
        cpu_stats = psutil.cpu_percent(interval=timeout_readings, percpu=True)
        for stat in cpu_stats:
            self.cpu_stats += str(stat) + ","

        average = round(sum(cpu_stats) / float(len(cpu_stats)), 2)
        self.cpu_stats += str(average) + "%"

        mem_stats = psutil.virtual_memory()
        self.mem_stats = Main.convert_size(mem_stats.total) + "," \
                         + Main.convert_size(mem_stats.used) + "," \
                         + Main.convert_size(mem_stats.free) + "," \
                         + str(round(100.0 - mem_stats.percent, 2)) + "%"

    def get_os_specific_stats(self):
        if platform.system() == 'Windows':
            w = wmi.WMI()
            # for el in w.Win32_TemperatureProbe():
            #     print(el)
            #
            # for el in w.Win32_VideoController():
            #     print(el)
            #
            # for el in w.Win32_Processor():
            #     print(el)
            #
            # for el in w.CIM_TemperatureSensor():
            #     print(el)

            # for el in w.Win32_Fan():
            #     print(el)

            for el in w.CIM_PCVideoController():
                if any(el.AdapterCompatibility in s for s in amd_names):
                    self.is_amd_card = True
                if any(el.AdapterCompatibility in s for s in nvidia_names):
                    self.is_nvidia_card = True
                if any(el.AdapterCompatibility in s for s in intel_names):
                    self.is_intel_card = True

            w2 = wmi.WMI(namespace="root\\wmi")
            try:
                temperature_info = w2.MSAcpi_ThermalZoneTemperature()
                print(temperature_info.CurrentTemperature)
            except wmi.x_wmi as wmi_e:
                print("Sorry, cannot handle wmi on this machine")
                print(wmi_e.com_error)
            except:
                print(sys.exc_info())

        else:
            sensors = psutil.sensors_temperatures()
            cpu_fan = psutil.sensors_fans()
            pass

    def get_gpu_stats(self):
        self.gpu_devices.clear()
        if self.is_amd_card:
            from gpu import AmdVideoCard
            amdCards = AmdVideoCard.AmdVideoCard.get_stats()
            self.gpu_devices.extend(amdCards)
        if self.is_nvidia_card:
            # TODO.md handle this
            pass
        if self.is_intel_card:
            # TODO.md handle this
            pass

    def connect(self):
        try:
            self.connection = serial.Serial(arduino_port, 115200, timeout=0)
            return True
        except serial.SerialException as e:
            print('Cannot connect to device %s %s', arduino_port, e)

    def send_to_aruduino(self, type_name, data, set_type_name_ending=True):
        self.connection.write(type_name.encode())

        if type(data) is int:
            self.connection.write(bytes([data]))
        elif type(data) is str:
            if set_type_name_ending:
                data += type_name + "_end"
            self.connection.write(data.encode())
        else:
            self.connection.write(data)

    def get_time(self):
        self.current_time = time.strftime(time_format, time.localtime(time.time()))
        self.uptime = str(datetime.strptime(self.current_time, time_format) \
                          - datetime.strptime(self.startup_time, time_format))
        self.day = str(time.strftime('%a', time.localtime(time.time())))


if __name__ == "__main__":
    main = Main()
    main.get_stats()
    main.get_time()
    main.get_os_specific_stats()
    main.get_gpu_stats()

    print("Starting up...\r\n")

    print("Cpu have: {} cores".format(main.cpu_count_real))
    print("Cpu have: {}  threads".format(main.cpu_count))
    print("Memory " + main.mem_stats)
    print("Cpu " + main.cpu_stats)
    print("Current time " + main.current_time)
    print("Uptime " + main.uptime)
    print("Day " + main.day)

    if len(main.gpu_devices) != 0:
        for device in main.gpu_devices:
            print("")
            print(device.adapterIndex + ": " + device.device_name)
            print("Fan load: " + device.fan_speed_percent)
            print("Fan rpm: " + device.fan_speed_rpm)
            print("Engine clock: " + device.eng_clock)
            print("Memory clock: " + device.mem_clock)
            print("Temperature: " + device.currtemp)
            print("Usage: " + device.usage)

    print("\r\n Sending information to device...")

    # if main.connect():
    # main.send_to_aruduino('cpu_cont', main.cpu_count_real)
    # main.send_to_aruduino('cpu_real', main.cpu_count)

    # while True:
    #     main.get_stats()
    #     main.get_time()
    #     main.get_gpu_stats()
    #     main.send_to_aruduino('cpu_stat', main.cpu_stats)
    #     main.send_to_aruduino('mem_stat', main.mem_stats)
    #     main.send_to_aruduino('current_time', main.current_time)
    #     main.send_to_aruduino('uptime', main.uptime)
    #     main.send_to_aruduino('curr_day', main.day)
    #     time.sleep(timeout_send)
