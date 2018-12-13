---
title: cartographer源码解析
date: 2018-08-08 19:43:14
tags: cartographer
category: slam技术
---
cartographer源码解析流程
<!-- more -->

AddNode

核心函数是ComputeConstraintsForNode,为节点添加约束，并且在后台开始扫描匹配.
node_id是分配的节点号，insertion_submap是允许插入的子地图，即最后两张，newly_finished_submap最后第二张子地图是否刚满（完成）
WorkItem::Result ComputeConstraintsForNode(node_id, insertion_submaps, newly_finished_submap);

ComputeConstraintsForNode

1. 把轨迹节点添加到optimization_problem_.
optimization_problem_->AddTrajectoryNode(
        matching_id.trajectory_id,
        optimization::NodeSpec2D{constant_data->time, local_pose_2d,
                                 global_pose_2d,
                                 constant_data->gravity_alignment})
2.遍历正在插入子图，填充图优化数据中的子地图数据和内部约束。                                 
data_.submap_data.at(submap_id).node_ids.emplace(node_id);
data_.constraints.push_back(
          Constraint{submap_id,
                     node_id,
                     {transform::Embed3D(constraint_transform),
                      options_.matcher_translation_weight(),
                      options_.matcher_rotation_weight()},
                     Constraint::INTRA_SUBMAP});
                     
trajectory_nodes_.at(node_id).constant_data
constant_data->local_pose()
submap.local_pose()
                     
constraint_transform
