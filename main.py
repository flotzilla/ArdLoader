from datetime import datetime

import psutil
import serial
import time
import math
import platform

if platform.system() == 'Windows':
    import wmi

arduino_port = 'COM11' # change it to your /dev/ttyACM[port] or /dev/ttyUSB[port] for linux or COM[port] for windows
timeout_readings = 1 # fix this
timeout_send = 0.01
time_format = "%H:%M %d/%m/%Y"


class Main:

    def __init__(self) -> None:
        self.mem_stats = self.cpu_stats = self.cpu_stats_total = None
        self.cpu_count_real = psutil.cpu_count(False)
        self.cpu_count = psutil.cpu_count()
        self.connection = None

        self.startup_time = time.strftime(time_format, time.localtime(psutil.boot_time()))
        self.current_time = self.uptime = self.day = None

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
                         + str(100.0 - mem_stats.percent) + "%"

    def get_os_specific_stats(self):
        if platform.system() == 'Windows':
            # w = wmi.WMI()
            # print(w.Win32_TemperatureProbe())
            # temperature_info = w.MSAcpi_ThermalZoneTemperature()[0]
            # print(temperature_info.CurrentTemperature)
            pass
        else:
            # psutil.sensors_temperatures()
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

    print("Starting up...\r\n")

    print("Cpu have: {} cores".format(main.cpu_count_real))
    print("Cpu have: {}  threads".format(main.cpu_count))
    print("Memory " + main.mem_stats)
    print("Cpu " + main.cpu_stats)
    print("Current time " + main.current_time)
    print("Uptime " + main.uptime)
    print("Day " + main.day)
    print("\r\n Sending information to device...")

    main.get_os_specific_stats()

    if main.connect():
        # main.send_to_aruduino('cpu_cont', main.cpu_count_real)
        # main.send_to_aruduino('cpu_real', main.cpu_count)

        while True:
            main.get_stats()
            main.get_time()
            main.send_to_aruduino('cpu_stat', main.cpu_stats)
            main.send_to_aruduino('mem_stat', main.mem_stats)
            main.send_to_aruduino('current_time', main.current_time)
            main.send_to_aruduino('uptime', main.uptime)
            main.send_to_aruduino('curr_day', main.day)
            time.sleep(timeout_send)
