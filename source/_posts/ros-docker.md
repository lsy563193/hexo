---
title: 安装docker的的ros
date: 2018-08-07 11:03:04
tags: 
- docker 
- ros
category: ros
---


## 1.安装docker过程
    https://yeasy.gitbooks.io/docker_practice/install/ubuntu.html

## 2.使用 Dockerfile 定制镜像

dockerfile
```
FROM osrf/ros:indigo-desktop-full

# # ARG ros_ip=172.117.0.1
ARG ros_ip=192.168.0.1
ENV ROS_IP=${ros_ip}  
ENV ROS_MASTER_URI=http://${ros_ip}:11311
COPY ./sources.list /etc/apt/sources.list

# RUN  apt-get update 
```