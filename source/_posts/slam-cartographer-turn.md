---
title: cartographer 调参日记
date: 2018-08-08 19:43:14
tags: cartographer
category: slam技术
---

cartographer 2d 调参

<!-- more -->
## 准备
使用1.0.0版本,因为公司扫地机用的是indigo版本,而我本机是用kinect版,所以我使用了docker来查看和调用rviz
Docker.indigo需要做些更改
- ARG CARTOGRAPHER_VERSION=release-1.0
- cmake 升级到3.2版以上
- 

## 调参
第一天
先从'/opt/ros/indigo/share/cartographer_ros/configuration',如果找不到再到'/usr/share/cartographer-ros'找
- map 通常是map
- **tracking_frame**: 由SLAM算法跟踪的帧的ROS帧ID。如果使用IMU，它应该在其位置，尽管它可能是旋转的。一个常见的选择是“imu_link”。 不明,不用imu,写了odom,
- **published_frame**: ROS帧ID用作发布姿势的子帧。例如，如果“odom”帧由系统的不同部分提供，则为“odom”。在这种情况下，map_frame中的“ odom ” 姿势将被发布。否则，将其设置为“base_link”可能是合适的。 不明,写了odom
- **odom_frame**: 仅在provide_odom_frame为true时使用。published_frame 和map_frame之间的框架，用于发布（非循环关闭）本地SLAM结果。通常是“odom”。
- **provide_odom_frame**: 如果启用，则本地非闭环连续姿势将作为map_frame中的odom_frame发布。
- **use_odometry**: 如果启用，请在主题“ odom ”上订阅nav_msgs / Odometry。在这种情况下必须提供测距，并且信息将包含在SLAM中



2d

- use_imu_data  如果不用false
先关闭全局slam
- hit_probability 激光击中黑的程度
- miss_probability 激光击不中白的程度


online_correlative_scan_matching 更新initial_ceres_pose位置
ceres_scan_matcher_ pose_observation ,summary

