class GpuDevice(object):

    def __init__(self) -> None:
        self.device_name = None
        self.adapterIndex = None
        self.eng_clock = None
        self.mem_clock = None
        self.currtemp = None
        self.usage = None
        self.fan_speed_percent = None
        self.fan_speed_rpm = None
