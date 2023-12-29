# Create Lab x Swiss Cat+ - Efficient Station-to-Station Navigation of a Mobile Robot using Multi-Sensor Localisation

## Disclaimer
This package was copied from the private repository of Swiss Cat, to allow the review of the implemented code. It cannot be run unless one downloads the Nav2 package and the marvelmind packages. The package of interest is *mob_rob_loca*.

## Presentation
This package implements an accurate localization and navigation system of a wheeled-robot, the Edison mobile, in *ROS2 Galactic*. The localization uses an extended Kalman filter to fuse sensor data, specifically odometry of the wheels, ultrasonic GPS and IMU data. The navigation system was taken from the [Nav2 repository](https://github.com/ros-planning/navigation2/tree/galactic) and adapted to the needs of the SwissCat+ West Hub laboratory, where the Edison Mobile is operating and responsible of transporting vials between stations.

This file gives information on how to install and use the package. Some examples are also given to illustrate the package in action.

## Installation
In the terminal, write the following commands:
```
mkdir ~/edi_ws/src && cd ~/edi_ws/src
git clone git@github.com:Yanniscod/SwissCat_ROS2.git
rosdep install --from-paths src -y --ignore-src
cd ~/edi_ws
colcon build --symlink-install
```

As written, the package uses the full repository of [Nav2 repository](https://github.com/ros-planning/navigation2/tree/galactic) to navigate, but also the [robot_localization](https://github.com/automaticaddison/robot_localization) to compute the localization using the EKF. The first was fully cloned into the folder, as problems were experienced when trying to run the code using the operating system’s package manager, as suggested in the [Nav2 tutorial](https://navigation.ros.org/getting_started/index.html). Therefore, if you experience similar problems, please copy-paste the following commands in your terminal:
```
cd ~/edi_ws/src
git clone https://github.com/ros-planning/navigation2.git --branch galactic
cd ~/edi_ws
rosdep install -y -r -q --from-paths src --ignore-src --rosdistro galactic
colcon build --symlink-install
```

## Localization
The localization of the Edison robot is determined by fusing three sets of data: the ultrasonic GPS provided by [Marvelmind](https://marvelmind.com/product/starter-set-super-mp-3d/), the [bno055 IMU from Bosch](https://www.bosch-sensortec.com/products/smart-sensor-systems/bno055/) and the odometry of the wheels. One could have only used the GPS information to have the position of the robot, however when testing inside the laboratory, a large variance was observed as the signal was jumping back and forth. The following picture illustrates the trajectory seen by the raw GPS sensor, the odometry of the wheels and the odometry fused. 

INCLUDE GRAPH 

## On-robot communication
The Edison robot is composed of an arduino UNO controlling the DC motors. The latter is serial linked to a Raspberry 3B+, powering the IMU and GPS devices and communicating with the ROS2 server by subscribing to the velocity topic, /cmd_vel, and publishing the ticks of the motors, as well as IMU data. The GPS device has its own ROS2 node. 
The code uploaded on the Raspberry was put inside the /src and /launch folders of the mob_rob_loca package, and is recognised by starting with rpi_. The installation of the RPI will be documented in another README.
