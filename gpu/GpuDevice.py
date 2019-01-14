class GpuDevice(object):

    def __init__(self) -> None:
        self.device_name = None
        self.eng_clock = None
        self.mem_clock = None
        self.currtemp = None
        self.usage = None
        self.fan_speed_percent = None
        self.fan_speed_rpm = None

    def format(self, id=0):
        return 'dev_name' + self.device_name + 'dev_name_end' + \
               'eng_clock' + self.eng_clock + 'eng_clock_end' + \
               'mem_clock' + self.mem_clock + 'mem_clock_end' + \
               'currtemp' + self.currtemp + 'currtemp_end' + \
               'usage' + self.usage + 'usage_end' + \
               'fs_percent' + self.fan_speed_percent + 'fs_percent_end' + \
               'fs_rpm' + self.fan_speed_rpm + 'fs_rpm_end'
