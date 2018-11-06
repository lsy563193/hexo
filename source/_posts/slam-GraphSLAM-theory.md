---
title: graph slam 理论
date: 2018-11-05 11:03:04
tags: 
- cartographer 
category: slam技术
mathjax: true
---

graph slam 理论
<!-- more -->
## 什么是graph slam
图优化是比较常用的后端优化，cartographer也用到了这个方法。
假设有个一机器人，在初始位置$x_0$为0，先前移动1，看到了路标$l_0$为2，到达$x_2$的位置之后看到路标$l_0$的距离时0.8, 如图所示:

![graph_slam](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/grapher_slam.png)

从$x_0$到$x_1$的距离其实是不确定的，不能够以1来表示，因为会有误差，学过卡尔曼就知道他的概率分布其实是
$$
\frac{1}{\sqrt{2\pi\delta}}\exp^{1/2}\frac{(x_1 - x_0 - 1)^2}{\delta^2}
$$
是一个距离x0为1的正态分布。

上图中同样其他的边也是展示了这种节点与节点的约束.我们要做的就是通过建立这中约束然后通过这种约束求得最优解。
上图中有三种约束：

$$
x_0 : 0 \\
x_0 -> x_1: 1 \\
x_0 -> l_0: 2 \\
x_1 -> l_0: 0.8 
$$

其中$x_0=0$被称为"初始位姿约束"

$x_0 -> x_1: 1$被称为"初始位姿约束"

$x_0 -> l_0: 2 x_1 -> l_0: 0.8$ 为 "相对测量约束"

这些约束只有初始位姿约束时绝对的，所以在后面优化之后初始位姿不会变，这也要求初始位精度一定要高，不然后面的推断都会出错
## 推导过程
我们现在讲解一下求解最优值的过程，根据上面的约束，我们可以得到四个方程

$$
\left \lbrace
\begin{aligned}
    x_0 = 0 \\
    x_1 - x_0 -1 = 0 \\
    l_0 - x_0 - 2 = 0 \\
    l_0 - x_1 - 0.8 = 0
\end{aligned}
\right .
$$

使用最小二乘法

<!-- $$ -->
<!-- \underset{x}{min} \frac{1}{2}(||f_{i_1}(x_{i_1, ... , x_{i_k}})||^2) -->
<!-- $$ -->
$$
\underset{x}{min}\sum_i^4e() =  = (x_0)^2 + (x_1 - x_0 - 1)^2 + (l_0 - x_0 - 2)^2 + (l_0 - x_1 - 0.8)^2
$$

分别对$x_0$, $x_1$, $l_0$求偏导数

$$
\delta x
$$

## 矩阵

## 裁简


## 参考

[udacity ai-for robots 系列视频306到332](https://www.youtube.com/playlist?list=PLAwxTw4SYaPkCSYXw6-a_aAoXVKLDwnHK)

[graph slam tutorial : 从推导到应用1](https://blog.csdn.net/heyijia0327/article/details/47686523)

[深入理解图优化与g2o：图优化篇](https://www.cnblogs.com/gaoxiang12/p/5244828.html)

[Cartographer的原理探究——GraphSLAM理论基础](https://blog.csdn.net/jsgaobiao/article/details/65628918)