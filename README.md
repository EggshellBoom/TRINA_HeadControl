# TRINA HEAD CONTROLLER

This is the standalone version of the TRINA controller. It uses default WebSocket communication. It reads the headset orientation and controls the motors on the head accordingly. 

## Contents

[TOC]

## Code Outline
**WebSocket.py**
This file creates a WebSocket server and waits for the client(the VR headset) to connect. On open, it will instantiate servoController. On message, it will interpret the VR input, translates the headset orientations, and feed them to servoController.

**servoController.py**
This file implements the embedded code to control the head motors. It limits the motor motion to resemble a human head movement. A worth noting function:`reportServoState()`, when called, returns the motor angles in degrees`(tilt degree, pan degree)`. When executing the file alone, it emulates a Sin wave and moves the head motors according to the sinusoidal input.

## Hardware Setup 
Below are the lists of hardware that are included in the package.
1. Dynamixel Motor for tilt/pitch. ID: 1
2. Dynamixel Motor for pan/YAW. ID: 2
3. Zed Mini Camera
4. Ricoh Theta V Camera
5. U2D2 Controller Chip
6. 2 micro USB Cables
7. 3 USB Type-C Cables
8. U2D2 Power Adapter and Cable

To set up the hardware, simply connect the U2D2 chip to the computer(Windows/Linux) using one micro USB cable. 

After, connect the U2D2 chip to power using the power adaptor included.

To get the cameras' images, connect both cameras to the computer using 2 USB Type-C cables. One extra cable is provided for each type.


## Software Setup
A list of Python libraries should be installed before running the script. They are:

1. scipy
2. numpy
3. dynamixel_sdk
4. serial (for dynamicel_sdk internal usage, some installation comes with this built-in)
5. WebSocket(using the version aligned with the VR headset)
6. pandas(only for plotting the sin waves)

All of the libraries except for WebSocket is using the most updated version, so a simple pip install should get the job done :)

The only code one should modify to control the motors is line 39 of **servoController.py**. This line specifies which communication port is used. On a Windows machine, once the U2D2 chip is connected, one could find the COM port under the device manager.(Default 'COM1'). On Linux, the default is '/dev/ttyUSB0'. One can open the terminal and type: `ls /dev/tty*` to find more details.



## Usage
Once both setups are ready. Follow the below instructions to test the system:

1. turn on the U2D2 chip power switch
2. run `python WebSocket.py `
3. open the VR app, this would automatically connect to the WebSocket server, once connected, a servoController is instantiated and one should see the head moving to the initialized state and stay there. This state resembles a front looking and upright positioned human head.
4. start moving the VR headset around to see the head robot following the human movement.
5. to read the current angle/state of the head motors, call `servoController.reportServoState()` inside the websocket events from **WebSocket.py**.
6. To test the head controller without using the VR headset. run `python servoController.py `. This emulates a Sin wave and moves the head according to the sinusoidal input.


## Demo
You can find a demo of the head movement here:
https://youtu.be/FXgkCbaXvao



