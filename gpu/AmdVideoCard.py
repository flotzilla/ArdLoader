from pyadl import *
from gpu import GpuDevice


class AmdVideoCard:

    @staticmethod
    def get_stats():
        devices = []
        for el in ADLManager.getInstance().getDevices():
            device = GpuDevice.GpuDevice()
            device.device_name = el.adapterName.decode()
            core_freq_min, core_freq_max = el.getEngineClockRange()
            device.eng_clock = str(int(el.getCurrentEngineClock())) + "/" + str(int(core_freq_max)) + "Mhz"

            device.currtemp = str(int(el.getCurrentTemperature())) + "C"

            mem_freq_min, mem_freq_max = el.getMemoryClockRange()
            device.mem_clock = str(int(el.getCurrentMemoryClock())) + "/" + str(int(mem_freq_max)) + "Mhz"

            device.usage = str(el.getCurrentUsage()) + "%"

            fan_speed_percent_min, fan_speed_percent_max = el.getFanSpeedRange(ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE)
            device.fan_speed_percent = str(el.getCurrentFanSpeed(ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE)) + "%"

            fan_speed_rpm_min, fan_speed_rpm_max = el.fanSpeedRPMRange
            device.fan_speed_rpm = str(el.getCurrentFanSpeed(ADL_DEVICE_FAN_SPEED_TYPE_RPM)) \
                                   + "/" + str(fan_speed_rpm_max) + "RPM"

            devices.append(device)
        return devices
