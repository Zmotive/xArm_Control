# xArm_Control
Used to Control Lobot xArm

## Wiring
if you are using an FTDI programer. the pin out to the Robot is:
```
1 FTDI Black(GND) -> 1 GND ROBOT
4 FTDI Yellow(Rx) -> 2 Tx ROBOT
5 FTDI Orange(Tx) -> 3 Rx ROBOT
```

here is a diagram of it: https://images.app.goo.gl/7BeaCJrG1jQAY42o8

the pins of the xArm are labled right next to the headers but GND is closest to the arm.

## Installation

The requirements are python version 3 and the packages in the requirements.txt.

This can be installed with:

```pip3 install -r requirements.txt```

## Running the example.py
***WARNING: This is a robot and can pinch fingers and will move with this code***

Once example.py runs the robot should stand completely straight as this is the registered 0 position (reaching for the sky as straight as possible). If your robot does not do that. make sure to rotate the hubs of the motors so that it is set that way.

after it goes to zero, and a button is pressed, the robot will go to a 90 bent position on motor ID 4.

Do be mindful of your fingers as this robot is quite powerful for its size.

The output on the screen is mostly for diagnostics but is the bytes (in text form)  of what is being sent over the serial and also of what is received.

U = x55

```
Command Bytes: b'UU\t\x15\x06\x01\x02\x03\x04\x05\x06'
Returned Message: b'UU\x15\x15\x06\x01\n\x02\x02\x13\x02\x03\xea\x01\x04\xe6\x03\x05i\x02\x06\xcd\x01'
Command Bytes: b'UU\x17\x03\x06\xe8\x03\x01\xf4\x01\x02\x12\x02\x03\xe0\x01\x04\xe5\x01\x05\xf4\x01\x06\xcc\x01'
Command Bytes: b'UU\t\x15\x06\x01\x02\x03\x04\x05\x06'
Returned Message: b'UU\x15\x15\x06\x01\t\x02\x02\x13\x02\x03\xe3\x01\x04\xe3\x01\x05\xf5\x01\x06\xcd\x01'
```

if your robot is not communicating then there will only be commanded bytes.


