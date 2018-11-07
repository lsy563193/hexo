---
title: Ceres-solver examples之pose_graph_2d学习笔记
date: 2018-11-06 15:25:06
tags: 
- cartographer 
category: slam技术
mathjax: true
---
```cpp
// Constructs the nonlinear least squares optimization problem from the pose
// graph constraints.
void BuildOptimizationProblem(const std::vector<Constraint2d>& constraints,
                              std::map<int, Pose2d>* poses,
                              ceres::Problem* problem) {
  CHECK(poses != NULL);
  CHECK(problem != NULL);
  if (constraints.empty()) {
    LOG(INFO) << "No constraints, no problem to optimize.";
    return;
  }

  ceres::LossFunction* loss_function = NULL;
  ceres::LocalParameterization* angle_local_parameterization =
      AngleLocalParameterization::Create();

  for (std::vector<Constraint2d>::const_iterator constraints_iter =
           constraints.begin();
       constraints_iter != constraints.end(); ++constraints_iter) {
    const Constraint2d& constraint = *constraints_iter;

    std::map<int, Pose2d>::iterator pose_begin_iter =
        poses->find(constraint.id_begin);
    CHECK(pose_begin_iter != poses->end())
        << "Pose with ID: " << constraint.id_begin << " not found.";
    std::map<int, Pose2d>::iterator pose_end_iter =
        poses->find(constraint.id_end);
    CHECK(pose_end_iter != poses->end())
        << "Pose with ID: " << constraint.id_end << " not found.";

    const Eigen::Matrix3d sqrt_information =
        constraint.information.llt().matrixL();
    // Ceres will take ownership of the pointer.
    ceres::CostFunction* cost_function = PoseGraph2dErrorTerm::Create(
        constraint.x, constraint.y, constraint.yaw_radians, sqrt_information);
    problem->AddResidualBlock(
        cost_function, loss_function, &pose_begin_iter->second.x,
        &pose_begin_iter->second.y, &pose_begin_iter->second.yaw_radians,
        &pose_end_iter->second.x, &pose_end_iter->second.y,
        &pose_end_iter->second.yaw_radians);

    problem->SetParameterization(&pose_begin_iter->second.yaw_radians,
                                angle_local_parameterization);
    problem->SetParameterization(&pose_end_iter->second.yaw_radians,
                                angle_local_parameterization);
  }

  // The pose graph optimization problem has three DOFs that are not fully
  // constrained. This is typically referred to as gauge freedom. You can apply
  // a rigid body transformation to all the nodes and the optimization problem
  // will still have the exact same cost. The Levenberg-Marquardt algorithm has
  // internal damping which mitigate this issue, but it is better to properly
  // constrain the gauge freedom. This can be done by setting one of the poses
  // as constant so the optimizer cannot change it.
  std::map<int, Pose2d>::iterator pose_start_iter =
      poses->begin();
  CHECK(pose_start_iter != poses->end()) << "There are no poses.";
  problem->SetParameterBlockConstant(&pose_start_iter->second.x);
  problem->SetParameterBlockConstant(&pose_start_iter->second.y);
  problem->SetParameterBlockConstant(&pose_start_iter->second.yaw_radians);
}
```
Ceres-solver examples之pose_graph_2d学习笔记
ceres-solver库是google的非线性优化库，可以对slam问题，机器人位姿进行优化，使其建图的效果得到改善。pose_graph_2d是官方给出的二维平面上机器人位姿优化问题，需要读取一个g2o文件，运行程序后返回一个poses_original.txt和一个poses_optimized.txt，大家按字面意思理解，内部格式长这样：

```
pose_id x y yaw_radians
pose_id x y yaw_radians
pose_id x y yaw_radians
...

```
得到这两个文件后，用官方提供的plot_results.py可以画出原始和优化后的位姿地图
![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/ceres-pose-slam.png)
<!-- more -->

## 变量说明
重要变量为以下几个：
constraints：vector，放入变量的类型为Constraint2d， 含义为机器人两个pose之间的限制，Constraint2d包括两个pose的id，相对坐标x，y，和协方差阵。这个变量描述的是观测量测量量measurement，即机器人认为自己感知到的正确的数据。

poses: map类指针，键值对为id和 Pose2d ，Pose2d是一个由id，世界坐标x，y，yaw角。这个变量描述的是实际机器人的世界坐标位置，是确确实实发生的事实。

## 关键步骤
```cpp
    // Ceres will take ownership of the pointer.
    //将需要的参数传入，设置残差，构造costfunction，使用自动求导方式
    ceres::CostFunction* cost_function = PoseGraph2dErrorTerm::Create(
        constraint.x, constraint.y, constraint.yaw_radians, sqrt_information);
```
详情见下面的Costfunction的搭建。
### 一、Costfunction的搭建
使用ceres库的关键是构造 costfunction ，ceres官方搭建的costfunction，同样有一个类表示，名为PoseGraph2dErrorTerm，具体如下所示：
```cpp
class PoseGraph2dErrorTerm {
 public:
  PoseGraph2dErrorTerm(double x_ab, double y_ab, double yaw_ab_radians,
                       const Eigen::Matrix3d& sqrt_information)
      : p_ab_(x_ab, y_ab),
        yaw_ab_radians_(yaw_ab_radians),
        sqrt_information_(sqrt_information) {}
  template <typename T>
  //x_a,y_a(p_a)x_b,y_b(p_b)是世界下的ab坐标
  bool operator()(const T* const x_a, const T* const y_a, const T* const yaw_a,
                  const T* const x_b, const T* const y_b, const T* const yaw_b,
                  T* residuals_ptr) const {
    const Eigen::Matrix<T, 2, 1> p_a(*x_a, *y_a);
    const Eigen::Matrix<T, 2, 1> p_b(*x_b, *y_b);

    //map映射类  将外部传进来的residuals_ptr映射到matrix<3,1>，取名为residuals_map
    Eigen::Map<Eigen::Matrix<T, 3, 1> > residuals_map(residuals_ptr);

    residuals_map.template head<2>() =
        RotationMatrix2D(*yaw_a).transpose() * (p_b - p_a) -
        p_ab_.cast<T>();
    residuals_map(2) = ceres::examples::NormalizeAngle(
        (*yaw_b - *yaw_a) - static_cast<T>(yaw_ab_radians_));

    // Scale the residuals by the square root information matrix to account for
    // the measurement uncertainty.
    residuals_map = sqrt_information_.template cast<T>() * residuals_map;

    return true;
  }
  //静态成员函数 构造costfunction   AutoDiffCostFunction 残差参数为3维  其他参数每个1维(参数是operator里的参数)
  static ceres::CostFunction* Create(double x_ab, double y_ab,
                                     double yaw_ab_radians,
                                     const Eigen::Matrix3d& sqrt_information) {
    return (new ceres::AutoDiffCostFunction<PoseGraph2dErrorTerm, 3, 1, 1, 1, 1,
                                            1, 1>(new PoseGraph2dErrorTerm(
        x_ab, y_ab, yaw_ab_radians, sqrt_information)));
  }

  EIGEN_MAKE_ALIGNED_OPERATOR_NEW

 private:
  // The position of B relative to A in the A frame.
  const Eigen::Vector2d p_ab_;
  // The orientation of frame B relative to frame A.
  const double yaw_ab_radians_;
  // The inverse square root of the measurement covariance matrix.
  const Eigen::Matrix3d sqrt_information_;
};
```
其中包括：
一个构造函数PoseGraph2dErrorTerm(x_ab, y_ab, yaw_ab_radians, sqrt_information)；
一个运算符重载operator()(x_a, y_a, yaw_a, x_b, y_b, yaw_b, residuals_ptr)，其中residuals_ptr指向的东西是计算出的残差；
一个构造costfunction的函数Create(x_ab, y_ab, yaw_ab_radians,& sqrt_information)。

operator()的作用
传入参数计算残差，残差有三维，如下所示：
residual = information1/2 * [ raT * (pb - pa) - hat( pab ) ] （2维）
[ Normalize(yawb - yawa - hat( yawab ) ) ] （1维）


其中ra  是 timestep a 时从当前坐标系转向世界坐标系的旋转矩阵， pb  和 pa 是世界坐标系下timestep a 和 b 时的机器人位置，带hat的是测量值，是在时刻a时机器人坐标系下观察的测量值。

Create函数的作用
用来构造一个costfunction类，与一般不同的是，main函数里调用Create函数来构造costfunction.
定义求导方式，官方例程里定义的是自动求导方式，即ceres::AutoDiffCostFunction，<>里的参数是我们的PoseGraph2dErrorTerm类，和优化变量的维数，详情见代码注释。
### 二、构造Problem
当costfunction搭建好后，给每个constraint都加入残差快AddResidualBlock, 官方例程没有用核函数，传入costfunction，传入待优化参数即可。
```cpp
    //添加problem 待优化的参数和PoseGraph2dErrorTerm里的operator保持一致
    problem->AddResidualBlock(
        cost_function, loss_function, &pose_begin_iter->second.x,
        &pose_begin_iter->second.y, &pose_begin_iter->second.yaw_radians,
        &pose_end_iter->second.x, &pose_end_iter->second.y,
        &pose_end_iter->second.yaw_radians);
```
### 三、LocalParameterization搭建
理论详情见( https://blog.csdn.net/HUAJUN998/article/details/76222745 ），目的是利用一个增量构造Jacobian矩阵更新变量，具体不是很懂。官方例程只用它优化了yaw角，官方例程按照ceres库内的autodiff_local_parameterization.h定义方法定义了一个AngleLocalParameterization类，写在了例程中的angle_local_parameterization.h中，如下所示：
// Defines a local parameterization for updating the angle to be constrained in
// [-pi to pi).
class AngleLocalParameterization {
 public:

  template <typename T>
  bool operator()(const T* theta_radians, const T* delta_theta_radians,
                  T* theta_radians_plus_delta) const {
    *theta_radians_plus_delta =
        NormalizeAngle(*theta_radians + *delta_theta_radians);

    return true;
  }

  //构造LocalParameterization函数，使用自动求导
  //参数目前不懂什么意思，应该是operator中输入输出参数的维数，Global Size和Local size
  static ceres::LocalParameterization* Create() {
    return (new ceres::AutoDiffLocalParameterization<AngleLocalParameterization,
                                                     1, 1>);
  }
};

然后在主程序制造优化问题时，在迭代constraints之前就create了角度的localparameterization：
```cpp
  //构造yaw角度的localparameterization，更新角度 yaw_new = yaw + △yaw
  ceres::LocalParameterization* angle_local_parameterization =
      AngleLocalParameterization::Create();
```

等到迭代遍历时，就加入了每一个constraint内两个pose的yaw角，如下所示：
```cpp
    //为yaw角设置localparameterization
    problem->SetParameterization(&pose_begin_iter->second.yaw_radians,
                                angle_local_parameterization);
    problem->SetParameterization(&pose_end_iter->second.yaw_radians,
                                angle_local_parameterization);
```

### 四、固定初始位姿
官方例程上讲，优化问题是三个自由度的，没有造成互相之间完全的限制，这个问题叫做规范自由度（gauge freedom），详情见规范固定 ，具体不懂，反正按官方例程的意思是要固定第一个pose，不让它进行优化。
  // The pose graph optimization problem has three DOFs that are not fully
  // constrained. This is typically referred to as gauge freedom. You can apply
  // a rigid body transformation to all the nodes and the optimization problem
  // will still have the exact same cost. The Levenberg-Marquardt algorithm has
  // internal damping which mitigate this issue, but it is better to properly
  // constrain the gauge freedom. This can be done by setting one of the poses
  // as constant so the optimizer cannot change it.
  //规范固定，通过将一个pose设定成常量来限制规范自由度，具体含义不懂
```cpp
  std::map<int, Pose2d>::iterator pose_start_iter =
      poses->begin();
  CHECK(pose_start_iter != poses->end()) << "There are no poses.";
  problem->SetParameterBlockConstant(&pose_start_iter->second.x);
  problem->SetParameterBlockConstant(&pose_start_iter->second.y);
  problem->SetParameterBlockConstant(&pose_start_iter->second.yaw_radians);
```


五、相关链接
以上是程序的主要问题，关于cpp的基础知识可参考下方链接：
ceres-solver官方教程