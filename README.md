[![MIT License][license-shield]][license-url]

# ArdLoader

PC stats monitoring

## Description
This until gather PC's information (cpu, mem, video cards loading, fan stats) and send them via serial port

Device: [Arduino based project](https://github.com/flotzilla/WminiLoad) for displaying info on LCD 4x20 screen

## Current status
* show cpu and mem load
* support AMD video cards on Windows system (simply don't have any Nvidia card)

## Screenshots

**Console stats**

![console_init](https://user-images.githubusercontent.com/3332506/78721597-82ea3680-7930-11ea-93f8-671dab2160fc.png)

**Overall statistics (linux)**
![stats_image](https://user-images.githubusercontent.com/3332506/78722081-70bcc800-7931-11ea-81a5-37a7e3a127c5.jpg)
Lines:
1. CPU load
2. Memory usage
3. Current date
4. Uptime

**Overall statistics (windows)**
![stats_image](https://user-images.githubusercontent.com/3332506/78845554-89041400-7a11-11ea-8ca0-7d75aecd4009.jpg)
Lines:
1. CPU load
2. Memory usage
3. GPU fan usage, GPU temp, overall usage
4. Current date

**Load of each cpu**

![photo_2020-04-09_03-12-05](https://user-images.githubusercontent.com/3332506/78845122-5d345e80-7a10-11ea-90b1-5946b16e2505.jpg)

**GPU load**

![photo_2020-04-09_03-11-56](https://user-images.githubusercontent.com/3332506/78845177-881eb280-7a10-11ea-92a1-98202373c58f.jpg)
Lines:
1. Fan usage, RPM
2. Engine clock, temperature
3. Memory clock, usage
4. CPU load, memory usage, videocard number

## Preparations 
* set port name in config.py file
```python
# change it to your /dev/ttyACM[port] or /dev/ttyUSB[port] for linux or COM[port] for windows
serial_port = '/dev/ttyUSB0'
```
* or set hwid parameter for autodetect your device by hwid
    * You read this value from `lsusb` command in linux
    * or for windows, see device properties
    
```python
hwid = '1A86:7523'
```
    
![image](https://user-images.githubusercontent.com/3332506/78846004-fe241900-7a12-11ea-94af-9c9b32b9bd6f.png)

 
## Usage
 Tap button to change between screens. 
 Current screens: 
 * Overall statistics
 * CPU load for each core
 * GPU load (for each GPU will be separate screen)

## Requirements
linux:
* pyserial
* psutil
* pyadl
* tabulate

windows:
* pyserial
* psutil
* tabulate
* pypiwin32
* wmi
* pyadl

## Licence
The MIT License (MIT). Please see [License File](https://github.com/flotzilla/ArdLoader/blob/master/LICENCE.md) for more information.

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/flotzilla/ArdLoader/blob/master/LICENCE.md