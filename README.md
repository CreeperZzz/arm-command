# Arm-Command
## Project Members: Shiwei Hu, Lucas Katayama
### ECEM202A - Embedded Systems, Fall 2023


# Project Introduction

This project aims to allow an user to control smart home devices using their hands by simply pointing to it.

By using a raspberry pi, a camera, and a Lidar, we are able to first detect a person's fingers, create a depth map, and determine which object the user is pointing to. Then, with a simple command (such as saying "on/off") the smart home device will behave as expected. In addition, we plan on adding a laser pointer to provide the user a visual feedback to which object the system determined he/she is pointing to.

<img align="left" src="image1.png"> <br/><br/>


# Devices and Frameworks used

## Devices
1. Raspberry Pi
2. Raspberry Pi Camera
3. Intel Realsense L515
4. Servos
5. Laser Pointer

## Frameworks
1. MediaPipe's Hand landmark detection

