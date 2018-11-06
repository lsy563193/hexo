##LocalTrajectoryBuilder

Returns 'MatchingResult' when range data accumulation completed,
otherwise 'nullptr'. Range data must be approximately horizontal
for 2D SLAM. `TimedPointCloudData::time` is when the last point in
`range_data` was acquired, `TimedPointCloudData::ranges` contains the
relative time of point with respect to `TimedPointCloudData::time`.

### LocalTrajectoryBuilder 
AddImuData添加imuData

### extrapolator_
局部地图的位姿推断器。cartographer_ros不一样,addImuData时添加

### 雷达数据的处理过程

Node::HandleLaserScanMessage
SensorBridge::HandleLaserScanMessage
    ToPointCloudWithIntensities
    HandleLaserScan
    HandleRangefinder
CollatedTrajectoryBuilder  AddSensorData 
    AddData
Collator::AddSensorData
OrderedMultiQueue::Add
    Dispatch
    callback

global_trajectory_builder::AddSensorData
LocalTrajectoryBuilder2D::AddRangeData
RangeDataCollator::AddRangeData
    extrapolator_->ExtrapolatePose
    accumulated_range_data_
    TransformToGravityAlignedFrameAndFilter
AddAccumulatedRangeData
TransformRangeData
<!-- ScanMatch -->
<!-- InsertIntoSubmap -->
local_slam_result_callback_
OnLocalSlamResult
GetTrajectoryStates
scan_matched_point_cloud_publisher_


### Imu的处理过程

Node::HandleImuMessage
    sensor_samplers_ 分频，脉冲未到不处理
    extrapolators_.at(trajectory_id).AddImuData
SensorBridge::HandleImuMessage
CollatedTrajectoryBuilder::AddData
Collator::AddSensorData
OrderedMultiQueue::Add
BlockingQueue::Push, Dispatch callback
LocalTrajectoryBuilder2D::AddImuData
PoseExtrapolator::AddImuData
PoseGraph2D::AddImuData
OptimizationProblem2D::AddImuData

### Odometry的处理过程

Node::HandleOdometryMessage
    sensor_samplers_ 分频，脉冲未到不处理
    extrapolators_.at(trajectory_id).AddOdometryData  角速度和线速度
SensorBridge::HandleOdometryMessage
CollatedTrajectoryBuilder::AddData
Collator::AddSensorData
OrderedMultiQueue::Add
BlockingQueue::Push, Dispatch callback
LocalTrajectoryBuilder2D::AddOdometryData
PoseExtrapolator::AddOdometryData
PoseGraph2D::AddOdometryData
OptimizationProblem2D::AddOdometryData