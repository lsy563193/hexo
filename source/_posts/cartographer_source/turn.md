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
              
                                                    
              
              
              
