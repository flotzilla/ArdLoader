from pyadl import *

devices = ADLManager.getInstance().getDevices()
for device in devices:
    print("{0}. {1}".format(device.adapterIndex, device.adapterName))

    coreVoltageMin, coreVoltageMax = device.getCoreVoltageRange()
    print("\tEngine core voltage: {0} mV ({1} mV - {2} mV)".format(device.getCurrentCoreVoltage(), coreVoltageMin,
                                                                   coreVoltageMax))

    coreFrequencyMin, coreFrequencyMax = device.getEngineClockRange()
    print("\tEngine clock: {0} MHz ({1} MHz - {2} MHz)".format(device.getCurrentEngineClock(), coreFrequencyMin,
                                                               coreFrequencyMax))

    memoryFrequencyMin, memoryFrequencyMax = device.getMemoryClockRange()
    print("\tMemory clock: {0} MHz ({1} MHz - {2} MHz)".format(device.getCurrentMemoryClock(), memoryFrequencyMin,
                                                               memoryFrequencyMax))

    fanSpeedPercentageMin, fanSpeedPercentageMax = device.getFanSpeedRange(ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE)
    print("\tFan speed: {0} % ({1} % - {2} %)".format(device.getCurrentFanSpeed(ADL_DEVICE_FAN_SPEED_TYPE_PERCENTAGE),
                                                      fanSpeedPercentageMin, fanSpeedPercentageMax))

    fanSpeedRPMMin, fanSpeedRPMMax = device.fanSpeedRPMRange  # can use this, because device.getFanSpeedRange grab % and RPM in the same time
    # or also can use device.getFanSpeedRange(ADL_DEVICE_FAN_SPEED_TYPE_RPM)
    print("\tFan speed: {0} RPM ({1} RPM - {2} RPM)".format(device.getCurrentFanSpeed(ADL_DEVICE_FAN_SPEED_TYPE_RPM),
                                                            fanSpeedRPMMin, fanSpeedRPMMax))

    print("\tTemperature: {0} Celsius".format(device.getCurrentTemperature()))
    print("\tUsage: {0} %".format(device.getCurrentUsage()))