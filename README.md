# tos428py
Python configuration script for the TOS 428 controller board used in a retropie setup.


# Introduction

This project (tos428py) provides a python script to control the TOS GRS 428 controller board for use
in a retropie installation.

Details regarding the all-in-on TOS 428 kit are here: https://thunderstickstudio.com/products/tos-grs-4-to-8-way-restrictor-all-in-one-kit

This document assumes a retropie installation where the current user is `pi`.

The official software for configuratin the TOS 428 is here: https://github.com/SteBuTOS/tos428config-raspi

Other projects which can be used to configure the TOS 428 controller are:

- https://github.com/DaveBullet1050/BatoceraHelpers/
- https://github.com/ACustomArcade/tos428/


# Prerequisites

The tos428py package requires the pyserial python module to communicate with the TOS 428 controller board.
Use the following commands to install `pip3` which can then be used to install `pyserial`:

```
sudo apt-get install python3-pip
sudo pip3 install pyserial
```

# Install

Download the package using the following command:

```
cd /home/pi
git clone https://github.com/jrobertson98atx/tos428py.git
```

The script `tos428.py` can now be used to configure the TOS 428 controller board.

The script `runcommand-onlaunch.sh` can be used to automatically set the joystick way on game launch.
In order for retropie to use this script it needs to be in the config directory:

```
ln -s /home/pi/tos428py/runcommand-onlaunch.sh /opt/retropie/configs/all/
```

# Example Way Setup

The all-in-one kit has two templates which can can be used to determine if the angle
needs to be adjusted for 4 or 8 way setup. Here's an exmaple of setting the angles
using those templates; the actual angles needed will differ for each device.

Overlay the 8-way template to setup the 8-way angle. Check the orientation after each `setangle` command and iterate
until the template and restrictor are aligned.

```
./tos428.py getangle 8 
23

./tos428.py setangle 8 20
ok

./tos428.py setangle 8 19
ok

./tos428.py getangle 8
19
```

Overlay the 4-way template to setup the 4-way angle. Check the orientation after each `setangle` command and iterate
until the template and restrictor are aligned.

```
./tos428.py getangle 4 
81

./tos428.py setangle 4 79
ok

./tos428.py setangle 4 75
ok

./tos428.py setangle 4 73
ok

./tos428.py getangle 4
73
```

"Save" the new angles so they're not lost when power is removed.

```
./tos428.py makepermanent
ok
```
# Example Color Setup

Use this sequence to set the 4-way button color to Yellow and the 8-way button color to Blue:

```
./tos428.py setway 4
ok

./tos428.py getcolor 4
0,0,255

./tos428.py setcolor 4 255 255 0
ok

./tos428.py setway 8
ok

./tos428.py getcolor 8
255,0,0

./tos428.py setcolor 8 0 255 255
ok

./tos428.py makepermanent
ok
```



