# AdapterAPI
## Brief
Bring simple python-based API for interfacing [Step Motor Adapter](https://github.com/Sapieron/Step-motor-adapter-for-RPi).

This software was developed on Raspberry Pi4 as a host machine.

## Tools needed

### Software
- [Python 3](https://www.python.org/downloads/) installed on target machine.
### Hardware
- [Step-motor-adapter-for-RPi]() as a board to interface with. It must have the newest firmware flashed.
### Optional
- RS232 converter to use as UART master interface if other target board is being used

## Instalation
In order to download all neccesary libraries, a build_requirements.txt file has been created. In order to fetch run following command in terminal:
```Terminal
python3 -m pip install -r build_requirements.txt
```

It is also recommended to update gcc to newest version. On linux-based computers run:
```Terminal
sudo apt-get install gcc
```
## Target port configuration (Raspberry Pi4)
It is necessary to configure your UART port first to be able to send frames.

### Raspberry Pi4
As Adapter API is using ```Terminal /dev/ttyAMA0 ``` add these two lines at the end of your ```config.txt``` file: 
```
enable_uart=1
dtoverlay=miniuart-bt
```

Check [official RPi documentation](https://www.raspberrypi.org/documentation/configuration/uart.md)
for details and on how to configure UART ports.

### NVIDIA Jetson Nano
On NVIDIA Jetson Nano (assuming Jetpack SDK is installed) two steps are required:
1. execute following three commands:
``` Terminal
systemctl stop nvgetty 
systemctl disable nvgetty 
udevadm trigger
```
2. Add your user to group ```dialout```. Remember to logout and login for changes to take effect.

Credits:
- [post on www.jetsonhacks.com](https://www.jetsonhacks.com/2019/10/10/jetson-nano-uart/)
- [question on askubuntu.com](https://askubuntu.com/questions/210177/serial-port-terminal-cannot-open-dev-ttys0-permission-denied)

## Available commands
AdapterAPI class has following methods:
### General methods
- ```CMD_GetCurrentConfig()``` - Prints current port config to terminal.
- ```CMD_CheckConnection()``` - Sends acknowledgement command and returns true if succedded.
- ```CMD_ForceStopAll()``` - Forces to stop every movement of steppers, servos and pump
### Stepper-specific methods
- ```CMD_STEPPER_MoveToCoordinate(X, Y, Z)``` - Moves controlled cartesian coordinate system to specified position for 3 axis'. Takes 3 parameters, each meaning desired coordinate in [mm] of each axis. Parameters must be in range of -9999 to 9999.
- ```CMD_STEPPER_Rotate(X, Y, Z)``` - Rotates stepper motors by a specified number of rotations at the same time. Takes 3 parameters, each meaning desired number of rotations for each axis. Parameters must be in range of -9999 to 9999.
- ```CMD_STEPPER_SetCurrentPositionAsZero()``` - Sets current position of stepper motors to be zeroed. Useful after power-up.
- ```CMD_STEPPER_ForceStopMovement()``` - Forces to stop every movement of steppers. Returns true if succedded, False if not succeeded.
### Pump-specific methods
- ```CMD_PUMP_RotateForMs(time)``` - Rotates pump for desired time in [ms]. Parameter must be in range of -9999 to 9999.
- ```CMD_PUMP_FeedWater(mililiters)``` - Turns on water pump to pump desired amount of water in [ml]. Parameter must be in range of -9999 to 9999.
### Food-dispenser-specific methods
- ```CMD_DISPENSER_Rotate(FoodA, FoodB)``` - Rotates food dispensers by a set number or rotations.  Parameters must be in range of -9999 to 9999.

## Example usage

An example.py file has been written to demonstrate usage of all commands available in this library, it can be run as following:
```Terminal
python3 example.py
```