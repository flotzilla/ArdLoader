[![MIT License][license-shield]][license-url]

# ArdLoader

PC stats monitoring

## Description
-----------
This until gather PC's information (cpu, mem, video cards loading, fan stats) and send them via serial port
Device example: [Arduino project](https://github.com/flotzilla/WminiLoad) for displaying info on LCD screen

## Current status
------------
* show cpu and mem load
* supports AMD video cards on Windows system

## Screenshots
![console_init](https://user-images.githubusercontent.com/3332506/78721597-82ea3680-7930-11ea-93f8-671dab2160fc.png)

Console stats

![stats_image](https://user-images.githubusercontent.com/3332506/78722081-70bcc800-7931-11ea-81a5-37a7e3a127c5.jpg)

Device

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
The MIT License (MIT). Please see [License File](https://github.com/flotzilla/container/blob/master/LICENCE.md) for more information.

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/flotzilla/ArdLoader/blob/master/LICENCE.md