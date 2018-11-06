---
title: cartographer源码解析
date: 2018-08-08 19:43:14
tags: cartographer
category: slam技术
---
cartographer源码解析流程
<!-- more -->
流程:
整理轨迹生成器 > 添加数据
整理轨迹生成器 - > 处理传感器数据整理
collated_trajectory_builder| > AddData
collated_trajectory_builder| | > HandleCollatedSensorData
  global_trajectory_builder| | | > AddSensorData
local_trajectory_builder_2d| | | | > AddRangeData
        range_data_collator| | | | | > AddRangeData
local_trajectory_builder_2d| | | | | > InitializeExtrapolator
          pose_extrapolator| | | | | > GetLastPoseTime
          pose_extrapolator| | | | | > ExtrapolatePose
          pose_extrapolator| | | | | > ExtrapolatePose
          pose_extrapolator    call: 1574 times.
                           | | | | | > EstimateGravityOrientation
local_trajectory_builder_2d| | | | | > TransformToGravityAlignedFrameAndFilter
local_trajectory_builder_2d| | | | | > AddAccumulatedRangeData
          pose_extrapolator| | | | | | > ExtrapolatePose
local_trajectory_builder_2d| | | | | | > ScanMatch
          pose_extrapolator| | | | | | > AddPose
local_trajectory_builder_2d| | | | | | > InsertIntoSubmap
              pose_graph_2d| | | | > AddNode
              pose_graph_2d| | | | | > GetLocalToGlobalTransform
              pose_graph_2d| | | | | > AddTrajectoryIfNeeded
              pose_graph_2d| | | | | > AddWorkItem
              pose_graph_2d| | | | | | > ComputeConstraintsForNode
              pose_graph_2d| | | | | | | > InitializeGlobalSubmapPoses
      constraint_builder_2d| | | | | | | > ComputeSubmapPose
    optimization_problem_2d| | | | | | | > AddTrajectoryNode
      constraint_builder_2d| | | | | | | > ComputeSubmapPose
      constraint_builder_2d| | | | | | | > NotifyEndOfNode


              pose_graph_2d.cc:109 ]  4| | | | > AddNode
              pose_graph_2d.cc:250 ]  6| | | | | | > ComputeConstraintsForNode
              pose_graph_2d.cc:250 ]  6| | | | | | | > ComputeConstraint
              pose_graph_2d.cc:250 ]  6| | | | | | | | | > MaybeAddGlobalConstraint
              pose_graph_2d.cc:250 ]  6| | | | | | | | | | | > ComputeConstraint
              pose_graph_2d.cc:250 ]  6| | | | | | | | | | | | > Match
              
              pose_graph_2d.cc:250 ]  6| | | | | | | | > ComputeConstraintsForOldNodes
              pose_graph_2d.cc:250 ]  6| | | | | | | | | > ComputeConstraint
              pose_graph_2d.cc:250 ]  6| | | | | | | | | | > MaybeAddGlobalConstraint
              pose_graph_2d.cc:250 ]  6| | | | | | | | | | | > ComputeConstraint
              pose_graph_2d.cc:250 ]  6| | | | | | | | | | | | > Match
              
                                                    
              
              
              
