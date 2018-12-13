---
title: cartographer论文翻译:2d-lidar-slam的实时闭环
date: 2018-08-07 11:03:04
tags: 
- cartographer 
category: slam技术
mathjax: true
---
cartographer 论文翻译
<!-- more -->
## 摘要

LIDAR SLAM是获取平面地图的有效方法。  构建便携式捕获平台需要在有限的计算资源下操作。 我们介绍了我们的背包绘图平台中使用的方法，该平台实现了5厘米分辨率的实时构图和`闭环`。 为了实现实时`闭环`，我们使用branch-and-bound将扫描到Submap匹配计算为约束。

## I. 简介

本文的贡献是一种新的方法，用于降低计算激光数据的闭环约束的需求量。

## II. 相关工作

`Scan-to-scan matching`经常用于激光SLAM中计算相对姿态变化，例如[1] - [4]。 它的缺点是很快就会累积误差。

`Scan-to-map matching`有助于限制误差的累积。使用Gauss-Newton在线性插值地图上找到局部最优的一种方法是[5]。
在存在良好的位姿初始估计的情况下，在这种情况下通过使用足够高的数据速率LIDAR提供，局部优化的`Scan-to-map matching`是有效且稳健的。
在不稳定的平台上，使用惯性测量单元（IMU）将激光投影到水平面上以估计重力方向。

`pixel-accurate scan matching`方法，如[1]，进一步减少了局部误差累积。虽然计算上更昂贵，但这种方法对于`闭环检测`很有用。

一些方法着重于通过匹配激光扫描的`提取特征`来改善计算成本[4]。其他用于`闭环检测`方法包括`基于直方图的匹配`[6]，扫描数据中的`特征检测`，以及使用`机器学习`[7]。

`解决累积局部误差`的两种常用方法是`粒子滤波器`和`基于图形`的SLAM [2]，[8]。

`基于图形`的方法适用于表示位姿和特征的节点集合。 图中的边是由观察产生的约束。 可以使用各种优化方法来最小化由所有约束引入的误差，例如， [11]，[12]。
在[13]中描述了这种用于室外SLAM的系统，其使用基于图的方法，局部`scan-to-scan`匹配，以及基于Submap特征的直方图的重叠局部图的匹配。

## III. 系统概述

Cartographer可实时室内绘图，生成分辨率为5cm的2D网格地图。 `Laser scans`被插入到最优估算位姿的Submap中，假定在短时间内足够准确。 而`Scan match`发生在最近的`Submap`上，因此它只取决于最近的扫描，全局误差会累积。

cartographer `定期`运行`位姿优化`来减少误差积累。
当一个Submap完成时，就不会再将新的扫描插入其中，它将参与`Scan match`以获得`闭环`。
所有已完成的Submap和扫描都会自动考虑进行`闭环`。
如果它们基于当前的`位姿估计`足够`接近`，则`Scan match器`试图在Submap中找到扫描。
如果在当前`估计位姿`的`搜索窗口`中找到足够好的匹配，则将其作为`闭环约束`添加到`优化问题`。

通过每隔几秒完成一次优化，我们的经验就是当`重新访问位置`时`立即闭环`。
这导致了`软实时约束`，即`闭环Scan match`必须比添加新扫描更快，否则它会明显落后,闭环失败。
我们通过对每个完成的Submap使用`branch-and-bound`和几个`预先计算的网格`来实现这一点。

## IV. 局部2d slam


我们的系统将单独的局部和全局方法结合到2D SLAM中。
两种方法都优化了由LIDAR观测的（x，y）平移和旋转ξθ组成的姿态ξ=（ξx，ξy，ξθ），其进一步被称为`扫描`。
在不平的地面上，IMU用于估计重力方向，将扫描从水平安装的LIDAR投影到2D世界。
在我们的局部方法中，每个连续扫描与`Submap`相匹配，使用`非线性优化`将扫描与Submap对齐; 该过程称为` real time Scan match`,其随着时间累积误差，我们的全局方法将其去除，如第五节所述。


###  A. Scans

Submap构造是重复对齐scan和Submap坐标帧的迭代过程。
随着扫描的原点在$0 \in \Bbb R^2$，我们现在将关于扫描点的信息写为$H = \lbrace h_k\rbrace _{k=1,...,K}, h_k \in \Bbb R^2$。
Submap帧中扫描帧的姿态$\xi$表示为变换$T_\xi$，它将扫描点从扫描帧严格转换为Submap帧，定义为

$$
T_\xi = 
\underbrace{
\left(
    \begin {matrix}
        cos\xi_\delta & -sin\xi_\delta \\
        sin\xi_\delta & sin\xi_\delta
    \end{matrix} 
\right)}_{R_\xi}
p +
\underbrace{
\left(\begin {matrix} 
    \xi_x \\
    \xi_y
\end{matrix} \right)}_{t_\xi}.
\tag1
$$

### B. Submaps

一些连续扫描用于构建Submap。
这些Submap采用概率网格的形式$M : \gamma \Bbb Z × \gamma \Bbb Z \rightarrow [p_{min}, p_{max}]$，它以给定分辨率`r`的离散网格点进行映射，例如5厘米，到值。
这些值可以被认为是网格点被阻挡的概率。
对于每个网格点，我们将相应的`像素`定义为最接近该网格点的所有点。
每当要将扫描插入概率网格时，计算用于命中的一组网格点和用于未命中的不相交组。
对于每次击中，我们将最近的网格点插入到命中集中。
对于每个未命中，我们插入与每个像素相关联的网格点，该网格点与扫描原点和每个扫描点之间的一条光线相交，不包括已经在命中集中的网格点。
如果每个以前未观察到的网格点位于其中一个集合中，则会为其分配概率$p_{hit}$ 或 $p_{miss}$。
如果已经观察到网格点x，我们更新命中和未命中的几率
$$
odds(p) = \frac{p}{1-p}, \tag1
$$
$$
M_{new}(x) = clamp(odds^{-1}(odds(M_{old}(x))\cdot odds(p_{hit}))) \tag1
$$

and equivalently for misses

等同于未命中

![image](https://github.com/lsy563193/image/blob/master/cartographer_notes/carto_submap.png?raw=true)

### C. Ceres scan matching

在将扫描插入Submap之前，扫描位姿`ξ`相对于当前局部Submap进行优化（使用Ceresbased [14]Scan match器）。 扫描匹配器负责在Submap中的扫描点处找到`最大概率`的扫描位姿。 我们将其视为`非线性最小二乘问题`

$$
 \underset {\xi}{argmin} \sum_{k=1}^K(1-M_(smooth(T_\xi h_k)))^2
$$

其中$T\xi$根据扫描位姿将$h_k$从scan帧变换到Submap帧。
函数$M_{smooth} : \Bbb R^2 → \Bbb R$是局部Submap中概率值的平滑版本。
我们使用双三次插值。
结果，可以发生区间$[0, 1]$之外的值，但是被认为是无关紧要的。
这种平滑函数的数学优化通常比网格的分辨率提供更好的精度。
由于这是局部优化，因此需要良好的初始估计。
能够测量角速度的IMU可用于估计Scan match之间的位置的旋转分量$\theta$。
虽然计算密集程度更高，但可以在没有IMU的情况下使用更高频率的Scan match或像素精确扫描匹配方法。

## V. 闭环

由于扫描仅与包含少量最近扫描的Submap匹配，因此上述方法会慢慢累积误差。
对于仅几十次连续扫描，累积误差很小。
通过创建许多小Submap来处理更大的空间。
我们的方法，优化所有扫描和Submap的位姿，遵循`稀疏位姿调整`[2]。
插入扫描的相对位姿存储在内存中，以用于`闭环优化`。
除了这些相对位姿之外，一旦Submap不再发生变化，所有其他由scan和Submap组成的对都被认为是`闭环`。
global scan matcher在后台运行，如果找到良好匹配，则会将相应的相对位姿添加到优化问题中

### A. 优化问题

`闭环优化`，和`Scan match`一样，也被称为`非线性最小二乘问题`，它允许轻松添加残差以考虑其他数据。
每隔几秒钟，我们使用Ceres [14]来计算解决方案

$$
\underset{\Xi ^m,\Xi ^n}{argmin} \frac{1}{2}\sum _{ij}\rho (E^2(\xi _i^m,\xi _j^s;\sigma _{ij},\xi _{ij}))\tag{SPA}
$$

在给定一些约束的情况下，Submap构成$\Xi^m = \lbrace\xi_i^m\rbrace_{i=1,...,m}$和世界中的扫描构成$\Xi^s = \lbrace\xi_j^s\rbrace_{j=1,...,n}$被优化。
这些约束采用相对位姿$\xi_{ij}$和相关协方差矩阵$\Sigma_ij$的形式。
对于一对Submapi和扫描j，位姿ξij描述了Submap坐标系中Scan match的位置。
协方差矩阵Σij可以被评估，例如，遵循[15]中的方法，或者局部地使用Ceres [14]与（CS）的协方差估计特征。
这种约束的残差E由下式计算

$$
E^2(\xi_i^m, \xi_j^s;\Sigma_{ij},\xi_{ij}) = e(\xi_i^m,\xi_j^s;\xi_{ij})^T\Sigma_{ij}^{-1}e(\xi_i^m,\xi_j^s;\xi_{ij}),\tag4
$$
$$
e(\xi_i^m,\xi_j^s;\xi_{ij}) = \xi_{ij} - 
\left( 
    \begin{matrix} 
    R_{\xi_i^m}^{-1}(t_{\xi_i^m}-t_{\xi_j^s}) \\
    \xi_{ij} - \xi_{j;\theta}^s
    \end{matrix}
\right).\tag5
$$

损失函数$\rho$，例如`Huber loss`，用于减少当`Scan match`为优化问题添加不正确约束时可能出现在（SPA）中的异常值的影响。
例如，这可能发生在局部对称环境中，例如办公室隔间。
异常值的替代方法包括[16]。

### B. Branch-and-bound scan match

我们对最佳的`像素精确匹配`感兴趣
$$
\xi^* = \underset{\xi\in\omega}{argmax}\sum_{k=1}^kM_{nearest}(T_\xi h_k)),\tag{BBS}
$$

其中$\omega$是搜索窗口，$M_{nearest}$是M扩展到所有$\Bbb R^2$，首先将其参数四舍五入到最近的网格点，即将网格点的值扩展为相应的像素。使用（CS）可以进一步提高匹配的质量。

通过仔细选择步长来提高效率。
我们选择角度步长$\xi_\theta$，以便最大范围$d_{max}$的扫描点移动不超过$r$，即一个像素的宽度。
我们推导出使用余弦定律

$$
d_{max} = \underset{k=1,...,K}{max} \|h_k\|,\tag6 \\
$$
$$
\xi_\theta = arccos(1-\frac{r^2}{2d_max^2})\tag7
$$


我们计算了包含给定线性和角度搜索窗口大小的整数步骤，例如$W_x=W_y=7m$和$W_\theta=30\degree$
$$
w_x = \lceil\frac{W_x}{r}\rceil,\ w_y = \lceil\frac{W_y}{r}\rceil,\ w_\theta = \lceil\frac{W_\theta}{\xi_\theta}\rceil.\tag8
$$

这导致一个有限的集$W$形成一个围绕估计$\xi_\theta$放置在其中心的搜索窗口，
$$
\overline{W} = \{-w_x,...,w_x\} \times \{-w_y,...,w_y\} \times \{-w_\theta,...,w_\theta\}\tag9
$$
$$
W = \{\xi_0 + (rj_x, rj_y, \xi_\theta j_\theta):(j_x,j_y,j_\theta) \in \overline{W}\}\tag{10}
$$

找到$\xi^*$的朴素算法很容易制定，参见算法1，但对于搜索窗口大小，我们考虑到它会太慢。

![image](https://github.com/lsy563193/image/blob/master/cartographer_notes/algo1.png?raw=true)

相反，我们使用branch-and-bound在较大的搜索窗口上有效地计算$\xi^*$。
有关通用方法，请参见算法2。
    这种方法最初是在混合整数线性程序的背景下提出的[17]。
关于这个主题的文献很广泛; 见[18]简短概述。
主要思想是将可能性子集表示为树中的节点，其中根节点表示所有可能的解决方案，在我们的示例中为$W$。
每个节点的子节点形成其父节点的分区，因此它们一起表示同一组可能性。
叶节点是单体; 每个代表一个可行的解决方案。
请注意，算法是准确的。
只要内部节点c的得分（c）是其元素得分的上限，它就提供与朴素方法相同的解决方案。
在这种情况下，每当节点有界时，在该子树中不存在比目前最熟知的解决方案更好的解决方案。

为了得到具体的算法，我们必须决定节点选择，分支和上界计算的方法。

#### 1) 节点选择:

在没有更好的替代方案的情况下，我们的算法使用深度优先搜索（DFS）作为默认选择：算法的效率取决于被修剪的树的大部分。
这取决于两件事：良好的上限和良好的当前解决方案。
后一部分由DFS帮助，它可以快速评估许多叶节点。
由于我们不希望将不良匹配作为`闭环`约束添加，我们还引入了一个分数阈值，低于该分数阈值我们对最优解决方案不感兴趣。
由于实际上不会经常超过阈值，这降低了节点选择或找到初始启发式解决方案的重要性。
关于在DFS期间访问孩子的顺序，我们计算每个孩子的分数的上限，访问具有最大边界的最有希望的子节点。
算法3是这种方法。

#### 2) 分支规则：

树中的每个节点由整数元组$c=（c_x，c_y，c_θ，c_h）\in\Bbb Z^4$描述。
高度为ch的节点最多可合并$2^{ch}\times2^{ch}$可能的翻译，但代表一个特定的轮换：

$$
\overline {\overline{W}} = \Bigg(\{j_x,j_y\} \in \Bbb{Z}^2:  \\
\Big\lbrace
\begin{array}{l}
        c_x \leq j_x < c_x + 2^{ch} \\
        c_x \leq j_x < c_x + 2^{ch}
        \end{array}
\Big\rbrace
        \times \lbrace c_\theta \rbrace \Bigg) ,\tag{11}
$$

$$
\overline{W}_c = \overline{\overline{W}} \cap \overline{W}\tag{12}
$$
   

![image](https://github.com/lsy563193/image/blob/master/cartographer_notes/algo2.png?raw=true)

![image](https://github.com/lsy563193/image/blob/master/cartographer_notes/algo3.png?raw=true)

 
叶节点具有高度$c_h=0$，并且对应于可行解$W\ni\xi_c=\xi_0 +（rc_x，rc_y，\xi_\theta c_\theta）$。

在我们的算法3的公式中，包含所有可行解的根节点没有明确地出现并且分支到一组初始节点$C_0$，在固定高度$h_0$覆盖搜索窗口

$$
\overline{W}_{0,x} =  \lbrace -w_x + 2^{h_o}:j_x \in \Bbb Z, 0 \leq 2^{h_o} \leq 2w_x \rbrace, \\
\overline{W}_{0,x} =  \lbrace -w_x + 2^{h_o}:j_x \in \Bbb Z, 0 \leq 2^{h_o} \leq 2w_x \rbrace, \\
\overline{W}_{0,x} =  \lbrace -w_x + 2^{h_o}:j_x \in \Bbb Z, 0 \leq 2^{h_o} \leq 2w_x \rbrace, \\
C_0 = \overline{W}_{0,x} \times \overline{W}_{0,y} \times \overline{W}_{0,\theta} \times \{h_0\}. \tag{13}
$$

At a given node c with $c_h > 1$, we branch into up to four children of height $c_h − 1$
在$c_h>1$的给定节点c，我们分支最多四个子高度$c_h − 1$

$$
C_c = ((\{c_x,c_x + 2^{c_h-1}\} \times {c_y, c_y + 2^{c_h-1} \times c_\theta}) \cap \overline{W}) \times \{c_h-1\}\tag{14}
$$


#### 3) 计算上界： 
 
分支和边界方法的剩余部分是计算内部节点上限的有效方式，包括计算工作量和边界质量。
我们用

$$
score(c) = \sum_{k=1}^{K}\underset{j\in \overline{\overline{W_c}}}{max}M{nearest}(T\xi_jh_k) \\
\geq\sum_{k=1}^{K}\underset{j\in \overline{W_c}}{max}M_{nearest}(T\xi_{j}h_{k})\\
\underset{j\in \overline{W_c}}{max}\sum_{k=1}^{K}maxM_{nearest}(T\xi_{j}h_{k})\tag{15}
$$

为了能够有效地计算最大值，我们使用预先计算的网格$M_{precomp}^{ch}$。
每个可能的高度$c_h$预先计算一个网格允许我们用扫描点数的effor linear计算得分。
请注意，为了能够执行此操作，我们还计算了超过$\overline{\overline{W_c}}$的最大值，该值可能大于我们搜索空间边界附近的$\overline{W_c}$。

$$
score(c) = \sum_{k=1}^{K}M_{precomp}^{ch}(T\xi_{c}h_{k})\tag{16}
$$
$$
M_{precomp}^{ch}(x,y) =  
    \underset
    {\begin{matrix}
        x^, \in [x,x+r(2^h-1)] \\
        y^, \in [y,y+r(2^h-1)]
    \end{matrix}}
    {max}
M_{nearest}(x^, , y^,) \tag{17}
$$

与叶节点一样使用$\xi_c$。
请注意，Mhprecomp与$M_{nearest}$具有相同的像素结构，但在每个像素中存储从那里开始的$2^h\times 2^h$像素值的最大值。
图3给出了这种预先计算的网格的一个例子。

为了使构建预先计算的网格的计算工作量保持在较低水平，我们要等到概率网格不再接收更新。
然后我们计算一组预先计算的网格，并开始匹配它。

对于每个预先计算的网格，我们计算从每个像素开始的$2^h$像素宽行的最大值。
使用该中间结果，然后构造下一个预先计算的网格。

如果按照添加顺序删除值，则可以按摊销$O（1）$保持更改值集合的最大值。
连续最大值保存在一个双端队列中，可以递归地定义为包含当前在集合中的所有值的最大值，然后是在第一次出现最大值之后所有值的连续最大值列表。
对于空的值集合，此列表为空。
使用此方法，可以在$O（n）$中计算预先计算的网格，其中n是每个预先计算的网格中的像素数。

计算上限的另一种方法是计算较低分辨率的概率网格，连续减半分辨率，见[1]。
由于我们的方法的额外内存消耗是可接受的，我们更喜欢使用较低分辨率的概率网格，这导致比（15）更差的界限，从而对性能产生负面影响。
## 参考

[1] E. Olson，`M3RSM：多对多分辨率Scan match`，载于IEEE国际机器人与自动化会议论文集（ICRA），2015年6月。

[2] K. Konolige，G。Grisetti，R。Kummerle，W。Burgard，B。Limketkai，¨和R. Vincent，``稀疏位姿调整`2D绘图`，在IROS，台湾台北，2010年10月10日。

[3] F. Lu和E. Milios，`用于环境绘图的全局一致范围扫描对准`，自主机器人，第一卷。 4，不。 4，pp.333- 349,1997。

[4]F.Mart'ın，R。Triebel，L。Moreno和R. Siegwart，`两种不同的三维构图工具：基于DE的Scan match和基于特征的环路检测`，Robotica，vol。 32，不。 01，pp.19-41,2014。

[5] S. Kohlbrecher，J。Meyer，O。von Stryk和U. Klingauf，`具有完整3D运动估计的灵活且可扩展的SLAM系统`，Proc。 IEEE国际安全，安全和救援机器人研讨会（SSRR）。 IEEE，2011年11月。

[6] M. Himstedt，J。Frost，S。Hellbach，H.-J。 Bohme和E. Maehle，`使用几何地标关系的2D LIDAR扫描中的大规模地点识别`，智能机器人和系统（IROS 2014），2014年IEEE / RSJ国际会议。 IEEE，2014，pp.5030-5035。

[7] K. Granstrom，T。B.Sch¨on，J.I。Nieto和F. T. Ramos，`学习close闭合范围数据循环`，`国际机器人研究杂志`，第一卷。 30，不。 14，pp.1728-1754,2011。

[8] G. Grisetti，C。Stachniss和W. Burgard，`通过自适应提议和选择性重采样改进基于网格的SLAM与Rao-Blackwellized粒子滤波器`，机器人与自动化，2005年.ICRA 2005. 2005年会议记录IEEE国际会议。 IEEE，2005，pp.2432-2437。

[9] G. D. Tipaldi，M。Braun和K. O. Arras，`FLIRT：2D范围数据的兴趣区域，应用于机器人导航`，在实验机器人中。 Springer，2014年，第695-710页。
