---
title: graph slam ceres 实现
date: 2018-08-07 11:03:04
tags: 
- cartographer 
category: slam技术
mathjax: true
---
本文是graph-slam 理论部分: ceres的实现部分
$$
e = (x_0)^2 + (x_1 - x_0 - 1)^2 + (l_0 - x_0 - 2)^2 + (l_0 - x_1 - 0.8)^2
$$

```c++
#include <vector>
#include <iomanip>
#include "ceres/ceres.h"
#include "gflags/gflags.h"
#include "glog/logging.h"

using ceres::AutoDiffCostFunction;
using ceres::CostFunction;
using ceres::Problem;
using ceres::Solver;
using ceres::Solve;

struct F1 {
  template <typename T> bool operator()(const T* const x1,
                                        const T* const x2,
                                        T* residual) const {
    // f1 = x0;
    residual[0] = x1[0];
    return true;
  }
};

struct F2 {
  template <typename T> bool operator()(const T* const x1,
                                        const T* const x0,
                                        T* residual) const {
    // f2 = (x1 - x0 -1.0)
    residual[0] = x1[0] - x0[0] - 1.0;
    return true;
  }
};

struct F3 {
  template <typename T> bool operator()(const T* const l0,
                                        const T* const x0,
                                        T* residual) const {
    // f3 = l0 - x0 - 2.0
    residual[0] = l0[0] - x0[0] - 2.0;
    return true;
  }
};

struct F4 {
  template <typename T> bool operator()(const T* const l0,
                                        const T* const x1,
                                        T* residual) const {
    // f4 = lo - x1 - 0.8
    residual[0] = l0[0] - x1[0] - 0.8;
    return true;
  }
};

DEFINE_string(minimizer, "trust_region",
              "Minimizer type to use, choices are: line_search & trust_region");

int main(int argc, char** argv) {
  CERES_GFLAGS_NAMESPACE::ParseCommandLineFlags(&argc, &argv, true);
  google::InitGoogleLogging(argv[0]);

  double x0 =  0.0;
  double x1 = 1.0;
  double l0 =  2.0;
//  double x4 =  1.0;

  Problem problem;
  // Add residual terms to the problem using the using the autodiff
  // wrapper to get the derivatives automatically. The parameters, x0 through
  // x4, are modified in place.
  problem.AddResidualBlock(new AutoDiffCostFunction<F1, 1, 1, 1>(new F1),
                           NULL,
                           &x0, &x1);
  problem.AddResidualBlock(new AutoDiffCostFunction<F2, 1, 1, 1>(new F2),
                           NULL,
                           &x1, &x0);
  problem.AddResidualBlock(new AutoDiffCostFunction<F3, 1, 1, 1>(new F3),
                           NULL,
                           &l0, &x0);
  problem.AddResidualBlock(new AutoDiffCostFunction<F4, 1, 1, 1>(new F4),
                           NULL,
                           &l0, &x1);

  Solver::Options options;
  LOG_IF(FATAL, !ceres::StringToMinimizerType(FLAGS_minimizer,
                                              &options.minimizer_type))
      << "Invalid minimizer: " << FLAGS_minimizer
      << ", valid options are: trust_region and line_search.";

  options.max_num_iterations = 100;
  options.linear_solver_type = ceres::DENSE_QR;
  options.minimizer_progress_to_stdout = true;

  std::cout << "Initial x0 = " << std::setprecision(4)<< x0
            << ", x1 = " << x1
            << ", l0 = " << l0
            << "\n";

  // Run the solver!
  Solver::Summary summary;
  Solve(options, &problem, &summary);

  std::cout << summary.FullReport() << "\n";
  std::cout << "Final x0 = " << x0
            << ", x1 = " << x1
            << ", l0 = " << l0
            << "\n";
  return 0;
}
```
[ceres-solver官网](http://ceres-solver.org/nnls_tutorial.html#powell-s-function)
