

# 🤖 Autonomous Navigation & SLAM with ROS 2

![ROS 2](https://img.shields.io/badge/ROS2-Humble-22314E?style=for-the-badge&logo=ros&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gazebo](https://img.shields.io/badge/Gazebo-11-orange?style=for-the-badge&logo=gazebo&logoColor=white)
![Platform](https://img.shields.io/badge/Ubuntu-22.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

## 📖 Project Overview
This project implements an **autonomous mobile robot** capable of navigating unknown environments without a pre-saved map. Developed for the **CEN449 - Introduction to Autonomous Robots** course, it utilizes the **TurtleBot3 Waffle Pi** platform within the Gazebo simulation environment.

The robot leverages **Lidar sensor data** to detect obstacles and makes real-time navigation decisions using a custom Python node, while simultaneously generating a 2D occupancy grid map via the **Google Cartographer SLAM** algorithm.

## ✨ Key Features
* **Reactive Navigation:** Custom Python algorithm (`otonom_surus.py`) for obstacle avoidance using raw LaserScan data.
* **Real-Time SLAM:** Simultaneous Localization and Mapping using Google Cartographer.
* **High-Performance Communication:** Configured with **CycloneDDS** middleware to resolve standard ROS 2 discovery and latency issues.
* **Simulation:** Fully simulated physics environment in Gazebo Classic.

## 🛠️ System Architecture
The system consists of three main nodes communicating over ROS 2 topics:
1.  **Simulation Node:** Gazebo (Publishes `/scan`, `/odom`, `/tf`).
2.  **SLAM Node:** Cartographer (Consumes `/scan`, publishes `/map`).
3.  **Control Node:** Custom Python script (Consumes `/scan`, publishes `/cmd_vel`).

## 🚀 Installation & Usage

### Prerequisites
* Ubuntu 22.04 LTS
* ROS 2 Humble Hawksbill
* TurtleBot3 Packages
* CycloneDDS (`sudo apt install ros-humble-rmw-cyclonedds-cpp`)

### 1. Launch Simulation Environment
Initialize the Gazebo world with the Waffle Pi model and CycloneDDS configuration:
```bash
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=waffle_pi
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
