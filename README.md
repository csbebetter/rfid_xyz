# rfid_xyz::Multi-antenna to realize the positioning and tracking of tags

## Introduction
In this code, we use the impinj reader and write the code based on the official ltkcpp library.
This code has many deficiencies and specifications, and will be gradually revised and improved

## Getting started
### Requirements
Please configure **ROS** and **python**
```shell
mkdir -p ~/catkin_ws/src
cd src
catkin_init_workspace
# Clone the files in src into the src directory you created
cd ~/catkin_ws/
catkin_make
```
### running
Before using this code, please manually calibrate the position of the antenna and the initial position of the tag
In files: ```src/rfid_reader/script/Levenberg_Marquarelt_algorithm.py``` ```src/rfid_reader/ltkcpp/include/RFIDHandler.h```
```shell
roscore
rosrun rfid_reader rfid_publisher
rosrun rfid_reader phase_xyz.py
```
