---
title: cartographer源码解析之sensor
date: 2018-08-08 19:43:14
tags: cartographer
category: slam技术
---

cartographer源码解析之sensor
<!-- more -->
## 目录解析

ImuTracker:  使用IMU的角速度和线性加速度跟踪方向。 因为平均线性加速度（假设慢速运动）是重力的直接测量，所以滚动/俯仰不会漂移，尽管是偏航。

Map_build: 使用用于局部子图TrajectoryBuilders和用于闭环的PoseGraph来连接整个SLAM堆栈。
成员只有五个  MapBuilderOptions; thread_pool_; pose_graph_; CollatorInterface sensor_collator_; trajectory_builders_ all_trajectory_builder_options_; ,其中pose_graph_用于全局优化，
  trajectory_builders_用于子地图构建. sensor_collator_ 用于数据收集
  我们先看sensor_collator_,
sensor_collator_ SensorInterface


##
  图优化

  [Real-time correlative scan matching 论文算法分析](https://blog.csdn.net/u012209790/article/details/82629422)
  [Cartographer 的前端算法思路](https://blog.csdn.net/u012209790/article/details/82735923)

  [cartographer Documentation](https://docs.ros.org/api/cartographer/html/classcartographer_1_1mapping_1_1constraints_1_1ConstraintBuilder2D.html)