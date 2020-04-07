from gpu.GpuDevice import GpuDevice
from serial import SerialException
from tabulate import tabulate

import serial.tools.list_ports
import sys
import time
import config as conf
import PcMetric

hwid = conf.hwid
serial_port = conf.serial_port


def detect_port_by_hwid(hardware_id):
    ports = list(serial.tools.list_ports.comports())
    found_port = None
    for p in ports:
        if hardware_id in p.hwid:
            found_port = p.device
    return found_port


if __name__ == "__main__":
    if detect_port_by_hwid(hwid) is not None:
        serial_port = detect_port_by_hwid(hwid)

    metric = PcMetric.PCMetric(serial_port, conf)
    metric.get_cpu_mem_stats()
    metric.get_time()
    metric.get_os_specific_stats()
    metric.get_gpu_stats()

    print("Starting up...")
    print(tabulate(
        [
            ["Cpu cores", metric.cpu_count_real],
            ['Cpu threads', metric.cpu_count],
            ['Memory load:', metric.cpu_count],
            ['Cpu load:', metric.trimmed_stats],
            ['Current time:', metric.current_time],
            ['Uptime', metric.uptime],
            ['Day', metric.day],
            ['Primary GPU:', conf.primary_gpu]
        ]
    ))

    if len(metric.gpu_devices):
        print('\n', "Showing video adapters info:")
        for index, device in enumerate(metric.gpu_devices):
            print(tabulate(
                [
                    [str(index), device.device_name],
                    ['Fan load', device.fan_speed_percent],
                    ['Fan rpm', device.fan_speed_rpm],
                    ['Engine clock', device.eng_clock],
                    ['Memory clock', device.mem_clock],
                    ['Temperature', device.currtemp],
                    ['Usage', device.usage]
                ]
            ))

    print("\r\nSending information to device", metric.port)

    if metric.connect():
        while True:
            try:
                metric.get_cpu_mem_stats()
                metric.get_time()
                metric.get_gpu_stats()

                metric.send_via_serial('cpu_stat', metric.trimmed_stats)
                metric.send_via_serial('cpu_count', str(metric.cpu_count_real))
                metric.send_via_serial('cpu_real', str(metric.cpu_count))
                metric.send_via_serial('va_count', str(len(metric.gpu_devices)))  # video adapters count
                metric.send_via_serial('prim_gpu', str(conf.primary_gpu))
                metric.send_via_serial('mem_stat', metric.mem_stats)
                metric.send_via_serial('current_time', metric.current_time)
                metric.send_via_serial('uptime', metric.uptime)
                metric.send_via_serial('curr_day', metric.day)

                va_device: GpuDevice
                for index, va_device in enumerate(metric.gpu_devices):
                    metric.send_via_serial('va' + str(index), va_device.format(index))

                time.sleep(conf.timeout_send)
            except KeyboardInterrupt as ke:
                print('\r\n', 'done')
                # TODO add clean screen operation
                sys.exit(1)
            except SerialException as se:
                print("Serial port writing error", se)
            except Exception as e:
                print(e)
