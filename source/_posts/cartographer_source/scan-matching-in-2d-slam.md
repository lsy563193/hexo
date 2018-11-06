##【泡泡机器人公开课】第二十三课：Scan Matching in 2D SLAM by 张明明

## 概述 Scan Matching
两类
Real-Time Loop Cloare in 2D LIDAR SLAM.ICRA2016,提到scan matching的两种方法


### scan-to-ccan --ICP,etc
- 计算成本大
- 累积误差,需进行闭环
- 容易进行闭环检测
### scan-to-map matching --Hector SLAM,etc
- 误差累积小计算成本小
- 难以闭环
更进一步的算法

## 2.ICP 
### PL-ICP(开源,ros)
典型的是PL-ICP,一般icp是点到点的二阶最小均平和(ICP variant using a point to linear metric ICRA2009),速度快,大的旋转不够鲁棒
公式:
论文:

### PL-ICP加闭环（g2o）
- 关键帧的选择策略
- 如何闭环
 对之前的关键帧进行搜索

- 1. 有一个大的旋转就选择一个关键帧
 缺点：没有submap(基于视觉的闭环),
- 2. 有个局部小闭环，
- 3. google 也是一个小闭环(不开源)
###　Hector Slam
