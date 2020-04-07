# mcu hwid, read this value from `lsusb` command in linux or set `serial_port` number value
hwid = '1A86:7523'

# change it to your /dev/ttyACM[port] or /dev/ttyUSB[port] for linux or COM[port] for windows
serial_port = '/dev/ttyUSB0'

# timeout reading of stats from pc
timeout_readings = 1

# interval of sleep time of main process
timeout_send = .3

# choose primary video card number under 'Showing video adapters info' line to display gpu stats on main screen
# set `primary_gpu = -1` to turn of this feature
primary_gpu = 0

# strings for parsing videocards data
amd_names = ['AMD', 'Advanced micro devices', 'Advanced Micro Devices, Inc.', 'Radeon']
nvidia_names = ['Nvidia']
intel_names = ['Intel Corporation', 'Intel']
