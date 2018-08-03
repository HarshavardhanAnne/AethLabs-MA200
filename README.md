# AethLabs MA200 RS232 Communication Module

This is a python2.7 module for the AethLabs MA200 device. The user manual
this module was written for can be found at this [link](https://aethlabs.com/microaeth/maX/operating-manual).

This module is intended for use on Linux distributions, and has only been tested on Debian based distros using python 2.7.

## Getting Started

The microAeth MA Series instruments are portable scientific instruments which measure the mass
concentration of light absorbing carbonaceous particles in a sampled aerosol. The MA200 communicates via four methods: USB 2.0, 3v3 TTL Serial, WiFi, Bluetooth Low Energy. This python module focuses on 3v3 ttl serial communcation.

## Prerequisites

### Materials

* 3v3 TTL Serial to USB Cable (comes with product)

### Software

Clone this repository using SSH(or download the .zip file)

```
git clone git@github.com:HarshavardhanAnne/AethLabs-MA200-serial.git
```

Install the python2.7 serial library

```
sudo apt-get install python-serial
```

Navigate to the cloned directory and copy ma200.py to the project directory you are working in

```
cp ma200.py /path/of/project/
```

## Serial Settings

The MA200 requires the following serial settings in order to communicate via serial:
* Baudrate: 1000000  
* Data Bits: 8  
* Parity: None  
* Stop Bits: 1  
* Flow Control: None (Xon/Xoff for firmware updates)

## How to Use

To use this module, the following inputs are required when creating an instance of this class:
* PORT: Linux serial port the unit is connected to, usually '/dev/ttyUSB0'
* PRINT_OPTION (optional): Enables or disables debug print statements (0 = Disabled, 1 = Enabled)

## Example

```
from ma200 import MA200

maObj1 = MA200('/dev/ttyUSB0')
maObj2 = MA200('/dev/ttyUSB0',1)

#Start serial connection
maObj1.open()

#Read data from device
data = maObj1.read()
if data is not None:
  print data

#Get the status of the serial connection
stat = maObj1.get_status()

#Get status code descriptions, returned as a list
descript = maObj1.get_status_code('1')
if descript is not None:
  print descript    # ["No status notifications"]

multi_des = maObj1.get_status_code('8','16','32')
if multi_des is not None:
  print multi_des # ["N/A","Optical saturation","Sampling timing error"]

#Returns the most recent data received from the device
recent_data = maObj1.get_most_recent()
if recent_data is not None:
  print recent_data

#Close serial connection
maObj1.close()
```

## Notes

* The device takes a couple minutes to start sending data once you start measuring.
* The data is formatted in the following way:
```
Date,Time,Serial number,Datum ID,Session ID,Data format version,Firmware version,Date / Time GMT,Timezone offset,GPS lat,GPS long,GPS Speed,Timebase,Status,Battery,Accel X,Accel Y,Accel Z,Tape position,Flow setpoint,Flow total,Sample temp,Sample RH,Sample dewpoint,Int pressure,Int temp,Optical config,UV Sen1,UV Ref,UV ATN1,Blue Sen1,Blue Ref,Blue ATN1,Green Sen1,Green Ref,Green ATN1,Red Sen1,Red Ref,Red ATN1,IR Sen1,IR Ref,IR ATN1,UV BC1,Blue BC1,Green BC1,Red BC1,IR BC1,CKSUM
```
