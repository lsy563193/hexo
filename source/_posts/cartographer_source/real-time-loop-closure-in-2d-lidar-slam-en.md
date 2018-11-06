Real-Time Loop Closure in 2D LIDAR SLAM


## Abstract 摘要

Portable laser range-finders, further referred to as LIDAR, and simultaneous localization and mapping (SLAM) are an efficient method of acquiring as-built floor plans. Generating and visualizing floor plans in real-time helps the operator assess the quality and coverage of capture data. Building a portable capture platform necessitates operating under limited computational resources. We present the approach used in our backpack mapping platform which achieves real-time mapping and loop closure at a 5 cm resolution. To achieve realtime loop closure, we use a branch-and-bound approach for computing scan-to-submap matches as constraints. We provide experimental results and comparisons to other well known approaches which show that, in terms of quality, our approach is competitive with established techniques.

LIDAR SLAM是获取平面地图的有效方法。 实时生成和可视化楼层平面图有助于评估捕获数据的质量和覆盖范围。 构建便携式捕获平台需要在有限的计算资源下操作。 我们介绍了我们的背包绘图平台中使用的方法，该平台实现了5厘米分辨率的实时构图和＂闭环＂。 为了实现实时＂闭环＂，我们使用branch-and-bound将扫描到Submap匹配计算为约束。 我们提供实验结果并与其他众所周知的方法进行比较，这些方法表明，在质量方面，我们的方法与已有技术相比具有竞争力。

## I. INTRODUCTION 简介
As-built floor plans are useful for a variety of applications.
Manual surveys to collect this data for building management tasks typically combine computed-aided design (CAD) with laser tape measures. 
These methods are slow and, by employing human preconceptions of buildings as collections of straight lines, do not always accurately describe the true nature of the space.
Using SLAM, it is possible to swiftly and accurately survey buildings of sizes and complexities that would take orders of magnitude longer to survey manually.
Applying SLAM in this field is not a new idea and is not the focus of this paper.
Instead, the contribution of this paper is a novel method for reducing the computational requirements of computing `loop closure constraints` from laser range data. 
This technique has enabled us to map very large floors, tens-of-thousands of square meters, while providing the operator fully optimized results in real-time.

竣工平面图适用于各种应用。
用于收集建筑物管理任务的数据的人工调查通常将计算机辅助设计（CAD）与激光卷尺相结合。
这些方法很慢，并且通过将人类对建筑物的偏见视为直线的集合，并不总是准确地描述空间的真实性质。
使用SLAM，可以快速准确地调查大小和复杂度的建筑物，这些建筑物需要花费更大的数量级才能手动调查。
在这个领域应用SLAM并不是一个新想法，也不是本文的重点。
相反，本文的贡献是一种新的方法，用于降低计算激光范围数据的闭环约束的计算要求。
这项技术使我们能够绘制数十万平方米的非常大的楼层，同时为操作员提供实时全面优化的结果。

## II. RELATED WORK 相关工作

`Scan-to-scan matching` is frequently used to compute relative pose changes in `laser-based` SLAM approaches, for example [1]–[4].
On its own, however, `scan-to-scan matching` quickly accumulates error.
`Scan-to-map matching` helps limit this accumulation of error. One such approach, which uses Gauss-Newton to find local optima on a linearly interpolated map, is [5].
In the presence of good initial estimates for the pose, provided in this case by using a sufficiently high data rate LIDAR, locally optimized `scan-to-map matching` is efficient and robust.
On unstable platforms, the laser fan is projected onto the horizontal plane using an inertial measurement unit (IMU) to estimate the orientation of gravity.
`Pixel-accurate `scan matching`` approaches, such as [1], further reduce local error accumulation.
Although computationally more expensive, this approach is also useful for `loop closure detection`.
Some methods focus on *improving on* the computational cost by matching on `extracted features` from the laser scans [4].
Other approaches (for `loop closure detection`) include `histogram-based matching` [6], `feature detection` in scan data, and using `machine learning` [7].
Two common approaches for `addressing the remaining local error accumulation` are `particle filter` and `graph-based` SLAM [2], [8].
`Particle filters` must maintain a representation of the full system state in each particle.
For `grid-based SLAM`, this quickly becomes resource intensive as maps become large; e.g. one of our test cases is 22,000 m2 collected over a 3 km trajectory.
Smaller dimensional feature representations, such as [9], which do not require a grid map for each particle, may be used to reduce resource requirements.
When an up-todate grid map is required, [10] suggests computing submaps, which are updated only when necessary, such that the final map is the rasterization of all submaps.
`Graph-based` approaches work over a collection of nodes representing poses and features.
Edges in the graph are constraints generated from observations.
Various optimization methods may be used to minimize the error introduced by all constraints, e.g. [11], [12].
Such a system for outdoor SLAM that uses a graph-based approach, local `scan-to-scan` matching, and matching of overlapping local maps based on histograms of submap features is described in [13].

`Scan-to-scan matching`经常用于激光SLAM中计算相对姿态变化，例如[1] - [4]。 然而，就其本身而言，`Scan-to-scan matching`很快就会累积误差。

`Scan-to-map matching`有助于限制误差的累积。使用Gauss-Newton在线性插值地图上找到局部最优的一种方法是[5]。
在存在良好的位姿初始估计的情况下，在这种情况下通过使用足够高的数据速率LIDAR提供，局部优化的`Scan-to-map matching`是有效且稳健的。
在不稳定的平台上，使用惯性测量单元（IMU）将激光投影到水平面上以估计重力方向。

`pixel-accurate scan matching`方法，如[1]，进一步减少了局部误差累积。虽然计算上更昂贵，但这种方法对于`闭环检测`也很有用。
一些方法着重于通过匹配激光扫描的`提取特征`来改善计算成本[4]。其他方法（用于`闭环检测`）包括`基于直方图的匹配`[6]，扫描数据中的`特征检测`，以及使用`机器学习`[7]。

`解决累积局部误差`的两种常用方法是`粒子滤波器`和`基于图形`的SLAM [2]，[8]。

`粒子滤波器`必须保持每个粒子中完整系统状态的表示。 对于`基于网格的SLAM`，随着地图变大，这很快变得资源密集;例如我们的一个测试案例是在3公里的轨道上收集了22,000平方米。 较小的维度特征表示，例如[9]，其不需要每个粒子的网格图，可用于减少资源需求。 当需要最新的网格图时，[10]建议计算Submap，仅在必要时更新，以便最终的图是所有Submap的光栅化。

`基于图形`的方法适用于表示位姿和特征的节点集合。 图中的边是由观察产生的约束。 可以使用各种优化方法来最小化由所有约束引入的误差，例如， [11]，[12]。
在[13]中描述了这种用于室外SLAM的系统，其使用基于图的方法，局部`scan-to-scan`匹配，以及基于Submap特征的直方图的重叠局部图的匹配。

## III. SYSTEM OVERVIEW 系统概述

`Google’s Cartographer` provides a real-time solution for indoor mapping in the form of a sensor equipped backpack that generates 2D grid maps with a r = 5 cm resolution.
The operator of the system can see the map being created while walking through a building.
`Laser scans` are inserted into a submap at the best `estimated position`, which is assumed to be sufficiently accurate for short periods of time.
`Scan matching` happens against a recent `submap`, so it only depends on recent scans, and the error of `pose estimates` in the world frame accumulates.
To achieve good performance with modest hardware requirements, our SLAM approach does not employ a `particle filter`.
To cope with the accumulation of error, we `regularly` run a `pose optimization`.
When a submap is finished, that is no new scans will be inserted into it anymore, `it takes part in `scan matching` for loop closure`.
All finished submaps and scans are automatically considered for loop closure.
If they are `close enough` based on current `pose estimates`, a `scan matcher` tries to find the scan in the submap.
If a sufficiently good match is found in a search window around the currently `estimated pose`, it is added as a `loop closing constraint` to the `optimization problem`.
By completing the optimization every few seconds, the experience of an operator is that `loops are closed immediately` when `a location is revisited`.
This leads to the `soft real-time constraint` that the `loop closure `scan matching`` has to `happen quicker` than `new scans are added`, otherwise it falls behind noticeably.
We achieve this by using a `branch-and-bound approach` and several `precomputed grids` per finished submap.

Cartographer可实时室内绘图，生成分辨率为5cm的2D网格地图。 `Laser scans`被插入到最优估算位置的Submap中，假定在短时间内足够准确。 而`Scan match`发生在最近的`Submap`上，因此它只取决于最近的扫描，全局误差会累积。

为了在适度的硬件要求下获得良好的性能，我们的SLAM方法不使用`粒子滤波器`。
cartographer `定期`运行`位姿优化`来减少误差积累。
当一个Submap完成时，就不会再将新的扫描插入其中，它将参与`Scan match`以获得`闭环`。
所有已完成的Submap和扫描都会自动考虑进行＂闭环＂。
如果它们基于当前的`位姿估计`足够`接近`，则`Scan match器`试图在Submap中找到扫描。
如果在当前`估计位姿`的`搜索窗口`中找到足够好的匹配，则将其作为`闭环约束`添加到`优化问题`。

通过每隔几秒完成一次优化，我们的经验就是当`重新访问位置`时`立即闭环`。
这导致了`软实时约束`，即`闭环Scan match`必须`比`添加新扫描更快`，否则它会明显落后,闭环失败。
我们通过对每个完成的Submap使用`branch-and-bound`和几个`预先计算的网格`来实现这一点。

## IV. LOCAL 2D SLAM 局部2d slam

Our system combines separate local and global approaches to 2D SLAM.
Both approaches optimize the pose, $\xi = (\xi_x, \xi_y, \xi_\delta)$ consisting of a $(x, y)$ translation and a rotation $\xi_\delta$, of LIDAR observations, which are further referred to as `scans`.
On an unstable platform, such as our backpack, an IMU is used to estimate the orientation of gravity for projecting scans from the horizontally mounted LIDAR into the 2D world. 
In our local approach, each consecutive scan is matched against a small chunk of the world, called a `submap M`, using a `non-linear optimization` that aligns the scan with the submap; this process is further referred to as `scan matching`. 
`Scan matching` accumulates error over time that is later removed by our global approach, which is described in Section V .


我们的系统将单独的局部和全局方法结合到2D SLAM中。
两种方法都优化了由LIDAR观测的（x，y）平移和旋转ξθ组成的姿态ξ=（ξx，ξy，ξθ），其进一步被称为`扫描`。
在不稳定的平面上，IMU用于估计重力方向，将扫描从水平安装的LIDAR投影到2D世界。
在我们的局部方法中，每个连续扫描与世界的一小块相匹配，称为`Submap`，使用`非线性优化`将扫描与Submap对齐; 该过程进一步称为`Scan match`。
`Scan match`随着时间累积误差，后来我们的全局方法将其去除，如第五节所述。

###  A. Scans
Submap construction is the iterative process of repeatedly aligning `scan` and `submap coordinate frames`, further referred to as `frames`.
With the origin of the scan at $0 \in \Bbb R^2$ , we now write the information about the scan points as $H = \lbrace h_k\rbrace _{k=1,...,K}, h_k \in \Bbb R^2$ . 
The pose $\xi$ of the scan frame in the submap frame is represented as the transformation $T_\xi$, which rigidly transforms scan points from the scan frame into the submap frame, defined as

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

A few consecutive scans are used to build a submap.
These submaps take the form of probability grids $M : \gamma \Bbb Z × \gamma \Bbb Z \rightarrow [p_{min}, p_{max}]$ which map from discrete grid points at a given resolution `r`, for example 5 cm, to values. 
These values can be thought of as the probability that a grid point is obstructed. 
For each grid point, we define the corresponding `pixel` to consist of all points that are closest to that grid point. 
Whenever a scan is to be inserted into the probability grid, a set of grid points for hits and a disjoint set for misses are computed. 
For every hit, we insert the closest grid point into the hit set. 
For every miss, we insert the grid point associated with each pixel that intersects one of the rays between the scan origin and each scan point, excluding grid points which are already in the hit set. 
Every formerly unobserved grid point is assigned a probability $p_{hit}$ or $p_{miss}$ if it is in one of these sets. 
If the grid point x has already been n observed, we update the odds for hits and misses as

$$
odds(p) = \frac{p}{1-p}, \tag1
$$
$$
M_{new}(x) = clamp(odds^{-1}(odds(M_{old}(x))\cdot odds(p_{hit}))) \tag1
$$

and equivalently for misses

等同于未命中

![image](/home/syue/github/cartographer-notes/docs/asset/carto_submap.png)

### C. Ceres `scan matching`

Prior to inserting a scan into a submap, the scan pose $\xi$ is optimized, relative to the current local submap,(using a Ceresbased [14] `scan matcher`). The `scan matcher` is responsible for finding a scan pose that `maximizes the probabilities` at the scan points in the submap. We cast this as a `nonlinear least squares problem`

在将扫描插入Submap之前，扫描位姿`ξ`相对于当前局部Submap进行优化（使用Ceresbased [14]Scan match器）。 扫描匹配器负责在Submap中的扫描点处找到`最大概率`的扫描位姿。 我们将其视为`非线性最小二乘问题`

$$
 \underset {\xi}{argmin} \sum_{k=1}^K(1-M_(smooth(T_\xi h_k)))^2
$$

where $T\xi$ transforms $h_k$ from the scan frame to the submap frame according to the scan pose.
The function $M_{smooth} : \Bbb R^2 → \Bbb R$ is a smooth version of the probability values in the local submap.
We use bicubic interpolation.
As a result, values outside the interval $[0, 1]$ can occur but are considered harmless.

其中$T\xi$根据扫描位姿将$h_k$从扫描帧变换到Submap帧。
函数$M_{smooth} : \Bbb R^2 → \Bbb R$是局部Submap中概率值的平滑版本。
我们使用双三次插值。
结果，可以发生区间$[0, 1]$之外的值，但是被认为是无害的。

Mathematical optimization of this smooth function usually gives better precision than the resolution of the grid.
Since this is a local optimization, good initial estimates are required. 
An IMU capable of measuring angular velocities can be used to estimate the rotational component $\theta$ of the pos between scan matches.
A higher frequency of scan matches or a `pixel-accurate `scan matching`` approach, although more computationally intensive, can be used in the absence of an IMU.

这种平滑函数的数学优化通常比网格的分辨率提供更好的精度。
由于这是局部优化，因此需要良好的初始估计。
能够测量角速度的IMU可用于估计Scan match之间的位置的旋转分量$\theta$。
虽然计算密集程度更高，但可以在没有IMU的情况下使用更高频率的Scan match或像素精确扫描匹配方法。

## V. CLOSING LOOPS 闭环

As scans are only matched against a submap containing a few recent scans, the approach described above slowly accumulates error. 
For only a few dozen consecutive scans, the accumulated error is small. 
Larger spaces are handled by creating many small submaps. 
Our approach, optimizing the poses of all scans and submaps, follows `Sparse Pose Adjustment` [2]. 
The relative poses where scans are inserted are stored in memory for use in the loop closing optimization. 
In addition to these relative poses, all other pairs consisting of a scan and a submap are considered for loop closing once the submap no longer changes. 
A `scan matcher` is run in the background and if a good match is found, the corresponding relative pose is added to the optimization problem

由于扫描仅与包含少量最近扫描的Submap匹配，因此上述方法会慢慢累积误差。
对于仅几十次连续扫描，累积误差很小。
通过创建许多小Submap来处理更大的空间。
我们的方法，优化所有扫描和Submap的位姿，遵循"稀疏位姿调整"[2]。
插入扫描的相对位姿存储在存储器中，以用于＂闭环＂优化。
除了这些相对位姿之外，一旦Submap不再发生变化，所有其他由扫描和Submap组成的对都被认为是＂闭环＂。
Scan match器在后台运行，如果找到良好匹配，则会将相应的相对位姿添加到优化问题中

### A. Optimization problem
`Loop closure` optimization, like `scan matching`, is also formulated as `a nonlinear least squares problem` which allows easily adding residuals to take additional data into account. 
Once every few seconds, we use Ceres [14] to compute a solution to

＂闭环＂优化，如`Scan match`，也被称为`非线性最小二乘问题`，它允许轻松添加残差以考虑其他数据。
每隔几秒钟，我们使用Ceres [14]来计算解决方案

$$
\underset{\Xi^m,\Xi^n}{argmin} \frac{1}{2}\sum_{ij}\rho(E^2(\xi _i^m,\xi _j^s;\sigma_{ij},\xi_{ij}))\tag{SPA}
$$

where the submap poses $\Xi^m = \lbrace\xi_i^m\rbrace_{i=1,...,m}$ and the scan poses $\Xi^s = \lbrace\xi_j^s\rbrace_{j=1,...,n}$ in the world are optimized given some constraints.
These constraints take the form of relative poses $\xi_{ij}$ and associated covariance matrices $\Sigma_ij$ . 
For a pair of submap i and scan j, the pose ξij describes where in the submap coordinate frame the scan was matched. 
The covariance matrices Σij can be evaluated, for example, following the approach in [15], or locally using the covariance estimation feature of Ceres [14] with (CS). 
The residual E for such a constraint is computed by

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


A loss function $\rho$, for example `Huber loss`, is used to reduce the influence of outliers which can appear in (SPA) when `scan matching` adds incorrect constraints to the optimization problem.
For example, this may happen in locally symmetric environments, such as office cubicles. 
Alternative approaches to outliers include [16]. 

损失函数$\rho$，例如`Huber loss`，用于减少当`Scan match`为优化问题添加不正确约束时可能出现在（SPA）中的异常值的影响。
例如，这可能发生在局部对称环境中，例如办公室隔间。
异常值的替代方法包括[16]。

### B. Branch-and-bound scan match

We are interested in the optimal, `pixel-accurate match`

我们对最佳的`像素精确匹配`感兴趣
$$
\xi^* = \underset{\xi\in\omega}{argmax}\sum_{k=1}^kM_{nearest}(T_\xi h_k)),\tag{BBS}
$$

where $\omega$ is the search window and $M_{nearest}$ is M extended to all of $\Bbb R^2$ by rounding its arguments to the nearest grid point first, that is extending the value of a grid points to the corresponding pixel.
The quality of the match can be improved further using (CS).

其中$\omega$是搜索窗口，$M_{nearest}$是M扩展到所有$\Bbb R^2$，首先将其参数四舍五入到最近的网格点，即将网格点的值扩展为相应的像素。使用（CS）可以进一步提高匹配的质量。

Efficiency is improved by carefully choosing step sizes. 
We choose the angular step size $\xi_\theta$ so that scan points at the maximum range $d_{max}$ do not move more than $r$, the width of one pixel. 
Using the law of cosines, we derive 

通过仔细选择步长来提高效率。
我们选择角度步长$\xi_\theta$，以便最大范围$d_{max}$的扫描点移动不超过$r$，即一个像素的宽度。
我们推导出使用余弦定律

$$
d_{max} = \underset{k=1,...,K}{max} \|h_k\|,\tag6 \\
$$
$$
\xi_\theta = arccos(1-\frac{r^2}{2d_max^2})\tag7
$$


We compute an integral number of steps covering given linear and angular search window sizes, e.g., $W_x = W_y = 7m$ and $W_\theta = 30\degree$

我们计算了包含给定线性和角度搜索窗口大小的整数步骤，例如$W_x=W_y=7m$和$W_\theta=30\degree$
$$
w_x = \lceil\frac{W_x}{r}\rceil,\ w_y = \lceil\frac{W_y}{r}\rceil,\ w_\theta = \lceil\frac{W_\theta}{\xi_\theta}\rceil.\tag8
$$

This leads to a finite set $W$ forming a search window around an estimate $\xi_\theta$ placed in its center,

这导致一个有限的集$W$形成一个围绕估计$\xi_\theta$放置在其中心的搜索窗口，
$$
\overline{W} = \{-w_x,...,w_x\} \times \{-w_y,...,w_y\} \times \{-w_\theta,...,w_\theta\}\tag9
$$
$$
W = \{\xi_0 + (rj_x, rj_y, \xi_\theta j_\theta):(j_x,j_y,j_\theta) \in \overline{W}\}\tag{10}
$$

A naive algorithm to find $\xi^*$ can easily be formulated, see Algorithm 1, but for the search window sizes we have in mind it would be far too slow . 

找到$\xi^*$的朴素算法很容易制定，参见算法1，但对于搜索窗口大小，我们考虑到它会太慢。
```
    algo
```

Instead, we use a branch and bound approach to efficiently compute $\xi^*$ over larger search windows. 
See Algorithm 2 for the generic approach. 
This approach was first suggested in the context of mixed integer linear programs [17]. 
Literature on the topic is extensive; see [18] for a short overview. 
The main idea is to represent subsets of possibilities as nodes in a tree where the root node represents all possible solutions, $W$ in our case. 
The children of each node form a partition of their parent, so that they together represent the same set of possibilities. 
The leaf nodes are singletons; each represents a single feasible solution. 
Note that the algorithm is exact. 
It provides the same solution as the naive approach as long as the score(c) of inner nodes c is an upper bound on the score of its elements. 
In that case, whenever a node is bounded, a solution better than the best known solution so far does not exist in this subtree. 

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

To arrive at a concrete algorithm, we have to decide on the method of node selection, branching, and computation of upper bounds.

为了得到具体的算法，我们必须决定节点选择，分支和上界计算的方法。

#### 1) Node selection:

Our algorithm uses depth-first search (DFS) as the default choice in the absence of a better alternative: The efficiency of the algorithm depends on a large part of the tree being pruned. 
This depends on two things: a good upper bound, and a good current solution. 
The latter part is helped by DFS, which quickly evaluates many leaf nodes. 
Since we do not want to add poor matches as loop closing constraints, we also introduce a score threshold below which we are not interested in the optimal solution. 
Since in practice the threshold will not often be surpassed, this reduces the importance of the node selection or finding an initial heuristic solution. 
Regarding the order in which the children are visited during the DFS, we compute the upper bound on the score for each child, visiting the most promising child node with the largest bound first. 
This method is Algorithm 3. 

1）节点选择：

在没有更好的替代方案的情况下，我们的算法使用深度优先搜索（DFS）作为默认选择：算法的效率取决于被修剪的树的大部分。
这取决于两件事：良好的上限和良好的当前解决方案。
后一部分由DFS帮助，它可以快速评估许多叶节点。
由于我们不希望将不良匹配作为＂闭环＂约束添加，我们还引入了一个分数阈值，低于该分数阈值我们对最优解决方案不感兴趣。
由于实际上不会经常超过阈值，这降低了节点选择或找到初始启发式解决方案的重要性。
关于在DFS期间访问孩子的顺序，我们计算每个孩子的分数的上限，访问具有最大边界的最有希望的子节点。
算法3是这种方法。

#### 2) Branching rule:

 Each node in the tree is described by a tuple of integers $c = (c_x, c_y, c_θ, c_h) \in \Bbb Z^4$. 
Nodes at height ch combine up to $2^{ch}\times2^{ch}$ possible translations but represent a specific rotation: 

2）分支规则：

树中的每个节点由整数元组$c=（c_x，c_y，c_θ，c_h）\in\Bbb Z^4$描述。
高度为ch的节点最多可合并$2^{ch}\times2^{ch}$可能的翻译，但代表一个特定的轮换：

$$
\overline {\overline{W}} = (\{j_x,j_y\} \in \Bbb{Z}^2:\\
        \left.
        \begin{array}{l}
        c_x \leq j_x < c_x + 2^{ch}\\
        c_x \leq j_x < c_x + 2^{ch}
        \end{array}
        \right\}
        \times \{c_\theta\},\tag11
$$

$$
\overline{W}_c = \overline{\overline{W}} \cap \overline{W}\tag{12}
$$

```
    algo2
```

```
    algo3
```
    
Leaf nodes have height ch = 0, and correspond to feasible solutions $W\ni \xi_c=\xi_0+(rc_x,rc_y,\xi_\theta c_\theta)$.

叶节点具有高度$c_h=0$，并且对应于可行解$W\ni\xi_c=\xi_0 +（rc_x，rc_y，\xi_\theta c_\theta）$。

In our formulation of Algorithm 3, the root node, encompassing all feasible solutions, does not explicitly appear and branches into a set of initial nodes $C_0$ at a fixed height $h_0$ covering the search window

在我们的算法3的公式中，包含所有可行解的根节点没有明确地出现并且分支到一组初始节点$C_0$，在固定高度$h_0$覆盖搜索窗口

$$
\overline{W}_{0,x} =  \{ -w_x + 2^{h_o}:j_x \in \Bbb Z, 0 \leq 2^{h_o} \leq 2w_x \} \\
\overline{W}_{0,x} =  \{ -w_x + 2^{h_o}:j_x \in \Bbb Z, 0 \leq 2^{h_o} \leq 2w_x \} \\
\overline{W}_{0,x} =  \{ -w_x + 2^{h_o}:j_x \in \Bbb Z, 0 \leq 2^{h_o} \leq 2w_x \} \\
C_0 = \overline{W}_{0,x} \times \overline{W}_{0,y} \times \overline{W}_{0,\theta} \times \{h_0\} \tag{13}
$$

At a given node c with $c_h > 1$, we branch into up to four children of height $c_h − 1$
在$c_h>1$的给定节点c，我们分支最多四个子高度$c_h − 1$

$$
C_c = ((\{c_x,c_x + 2^{c_h-1}\} \times {c_y, c_y + 2^{c_h-1} \times c_\theta}) \cap \overline{W}) \times \{c_h-1\}\tag{14}
$$


#### 3) Computing upper bounds: 
 
The remaining part of the branch and bound approach is an efficient way to compute upper bounds at inner nodes, both in terms of computational effort and in the quality of the bound.
We use
3）计算上界：

分支和边界方法的剩余部分是计算内部节点上限的有效方式，包括计算工作量和边界质量。
我们用

$$
score(c) = \sum_{k=1}^{K}\underset{j\in \overline{\overline{W_c}}}{max}M{nearest}(T\xi_jh_k) \\
\geq\sum_{k=1}^{K}\underset{j\in \overline{W_c}}{max}M_{nearest}(T\xi_{j}h_{k})\\
\underset{j\in \overline{W_c}}{max}\sum_{k=1}^{K}maxM_{nearest}(T\xi_{j}h_{k})\tag{15}
$$


To be able to compute the maximum efficiently, we use precomputed grids $M_{precomp}^{ch}$. 
Precomputing one grid per possible height $c_h$ allows us to compute the score with effor linear in the number of scan points. 
Note that, to be able to do this, we also compute the maximum over $\overline{\overline{W_c}}$ which can be larger than $\overline{W_c}$near the boundary of our search space.

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

with $\xi_c$ as before for the leaf nodes. 
Note that Mh precomp has the same pixel structure as $M_{nearest}$, but in each pixel storing the maximum of the values of the $2^h \times 2^h$ box of pixels beginning there. 
An example of such precomputed grids is given in Figure 3.
与叶节点一样使用$\xi_c$。
请注意，Mhprecomp与$M_{nearest}$具有相同的像素结构，但在每个像素中存储从那里开始的$2^h\times 2^h$像素值的最大值。
图3给出了这种预先计算的网格的一个例子。

To keep the computational effort for constructing the precomputed grids low, we wait until a probability grid will receive no further updates. 
Then we compute a collection of precomputed grids, and start matching against it. 

为了使构建预先计算的网格的计算工作量保持在较低水平，我们要等到概率网格不再接收更新。
然后我们计算一组预先计算的网格，并开始匹配它。

For each precomputed grid, we compute the maximum of a $2^h$ pixel wide row starting at each pixel. 
Using this intermediate result, the next precomputed grid is then constructed.

对于每个预先计算的网格，我们计算从每个像素开始的$2^h$像素宽行的最大值。
使用该中间结果，然后构造下一个预先计算的网格。

The maximum of a changing collection of values can be kept up-to-date in amortized $O(1)$ if values are removed in the order in which they have been added. 
Successive maxima are kept in a deque that can be defined recursively as containing the maximum of all values currently in the collection followed by the list of successive maxima of all values after the first occurrence of the maximum. 
For an empty collection of values, this list is empty. 
Using this approach, the precomputed grids can be computed in $O(n)$ where n is the number of pixels in each precomputed grids. 

如果按照添加顺序删除值，则可以按摊销$O（1）$保持更改值集合的最大值。
连续最大值保存在一个双端队列中，可以递归地定义为包含当前在集合中的所有值的最大值，然后是在第一次出现最大值之后所有值的连续最大值列表。
对于空的值集合，此列表为空。
使用此方法，可以在$O（n）$中计算预先计算的网格，其中n是每个预先计算的网格中的像素数。

An alternative way to compute upper bounds is to compute lower resolution probability grids, successively halving the resolution, see [1]. 
Since the additional memory consumption of our approach is acceptable, we prefer it over using lower resolution probability grids which lead to worse bounds than (15) and thus negatively impact performance.

计算上限的另一种方法是计算较低分辨率的概率网格，连续减半分辨率，见[1]。
由于我们的方法的额外内存消耗是可接受的，我们更喜欢使用较低分辨率的概率网格，这导致比（15）更差的界限，从而对性能产生负面影响。

## VI. EXPERIMENTAL RESULTS 实验结果


In this section, we present some results of our SLAM algorithm computed from recorded sensor data using the same online algorithms that are used interactively on the backpack. 
First, we show results using data collected by the sensors of our Cartographer backpack in the Deutsches Museum in Munich. 
Second, we demonstrate that our algorithms work well with inexpensive hardware by using data collected from a `robotic vacuum cleaner` sensor. 
Lastly, we show results using the `Radish data set` [19] and compare ourselves to published results.

在本节中，我们使用在背包上交互使用的相同在线算法，从记录的传感器数据中计算出我们的SLAM算法的一些结果。
首先，我们使用慕尼黑德意志博物馆的Cartographer背包传感器收集的数据显示结果。
其次，我们通过使用从`机器人真空吸尘器`传感器收集的数据证明我们的算法可以很好地与廉价的硬件配合使用。
最后，我们使用`萝卜数据集`[19]显示结果，并将自己与已发布的结果进行比较。

### A. Real-World Experiment: Deutsches Museum

Using data collected at the Deutsches Museum spanning 1,913 s of sensor data or 2,253 m (according to the computed solution), we computed the map shown in Figure 4. 
On a workstation with an Intel Xeon E5-1650 at 3.2 GHz, our SLAM algorithm uses 1,018 s CPU time, using up to 2.2 GB of memory and up to 4 background threads for loop closure `scan matching`. 
It finishes after 360 s wall clock time, meaning it achieved 5.3 times real-time performance. 
The generated graph for the loop closure optimization consists of 11,456 nodes and 35,300 edges. 
The optimization problem (SPA) is run every time a few nodes have been added to the graph. 
A typical solution takes about 3 iterations, and finishes in about 0.3 s.

使用在德意志博物馆收集的数据，跨越1,913秒的传感器数据或2,253米（根据计算的解决方案），我们计算出如图4所示的地图。
在具有3.2 GHz的Intel Xeon E5-1650的工作站上，我们的SLAM算法使用1,018秒的CPU时间，使用高达2.2 GB的内存和最多4个后台线程进行闭环Scan match。
它在360秒的挂钟时间后完成，这意味着它实现了5.3倍的实时性能。
生成的＂闭环＂优化图由11,456个节点和35,300个边组成。
每次向图表添加几个节点时都会运行优化问题（SPA）。
典型的解决方案需要大约3次迭代，并在大约0.3秒内完成。

### B. Real-World Experiment: Neato’s Revo LDS

Neato Robotics uses a laser distance sensor (LDS) called Revo LDS [20] in their vacuum cleaners which costs under $ 30. 
We captured data by pushing around the vacuum cleaner on a trolley while taking scans at approximately 2 Hz over its debug connection. 
Figure 5 shows the resulting 5 cm resolution floor plan. 
To evaluate the quality of the floor plan, we compare laser tape measurements for 5 straight lines to the pixel distance in the resulting map as computed by a drawing tool. 
The results are presented in Table I, all values are in meters. 
The values are roughly in the expected order of magnitude of one pixel at each end of the line.

Neato Robotics在其真空吸尘器中使用名为Revo LDS [20]的激光距离传感器（LDS），售价低于30美元。
我们通过推动手推车上的真空吸尘器捕获数据，同时通过其调试连接以大约2 Hz的速度进行扫描。
图5显示了5厘米分辨率的平面图。
为了评估平面图的质量，我们将5条直线的激光带测量结果与绘图工具计算得到的地图中的像素距离进行比较。
结果如表I所示，所有数值均以米为单位。
这些值大致在线的每一端的一个像素的预期数量级。

We compare our approach to others using the benchmark measure suggested in [21], which compares the error in relative pose changes to manually curated `ground truth` relations. 
Table II shows the results computed by our Cartographer SLAM algorithm. 
For comparison, we quote results for Graph Mapping (GM) from [21]. 
Additionally, we quote more recently published results from [9] in Table III. 
All errors are given in meters and degrees, either absolute or squared, together with their standard deviation. 
Each public data set was collected with a unique sensor configuration that differs from our Cartographer backpack. 
Therefore, various algorithmic parameters needed to be adapted to produce reasonable results. 
In our experience, tuning Cartographer is only required to match the algorithm to the sensor configuration and not to the specific surroundings.

我们使用[21]中建议的基准测量法将我们的方法与其他方法进行比较，后者将相对姿态变化的误差与手动策划的地面实况关系进行比较。
表II显示了我们的制图师SLAM算法计算的结果。
为了比较，我们引用[21]中的图形构图（GM）的结果。
此外，我们引用表III中最近公布的[9]结果。
所有误差均以米和度给出，绝对值或平方值，以及它们的标准偏差。
每个公共数据集都采用独特的传感器配置进行收集，该配置与我们的Cartographer背包不同。
因此，需要调整各种算法参数以产生合理的结果。
根据我们的经验，调整制图师只需要将算法与传感器配置相匹配，而不是与特定环境相匹配。



Since each public data set has a unique sensor configuration, we cannot be sure that we did not also fit our parameters to the specific locations. The only exception being the Freiburg hospital data set where there are two separate relations files. We tuned our parameters using the local relations but also see good results on the global relations.

由于每个公共数据集都有一个独特的传感器配置，我们无法确定，我们也不适合我们的参数到特定的位置。 唯一的例外是弗莱堡医院数据集，其中有两个独立的关系文件。 我们使用当地关系调整了参数，但也看到了全局关系的良好结果。


The most significant differences between all data sets is the frequency and quality of the laser scans as well as the availability and quality of odometry.
所有数据集之间最显着的差异是激光扫描的频率和质量以及测距的可用性和质量。

Despite the relatively outdated sensor hardware used in the public data sets, Cartographer SLAM consistently performs within our expectations, even in the case of `MIT CSAIL`, where we perform considerably worse than `Graph Mapping`.
For the Intel data set, we outperform `Graph Mapping`, but not `Graph FLIRT`. 
For MIT Killian Court we outperform `Graph Mapping` in all metrics. 
In all other cases, Cartographer outperforms both `Graph Mapping` and `Graph FLIRT` in most but not all metrics
尽管公共数据集中使用了相对过时的传感器硬件，但Cartographer SLAM始终如一地符合我们的预期，即使在`MIT CSAIL`的情况下，我们的表现也比`图谱构图`差得多。
对于英特尔数据集，我们优于`图形构图`，但不是`图形FLIRT`。
对于MIT Killian Court，我们在所有指标中都超越了`图形构图`。
在所有其他情况下，Cartographer在大多数但不是所有指标中都优于`图形构图`和`图形FLIRT`

Since we add `loop closure constraints` between submaps and scans, the data sets contain no `ground truth` for them. 
It is also difficult to compare numbers with other approaches based on `scan-to-scan`. 
Table IV shows the number of `loop closure constraints` added for each test case (true and false positives), as well as the precision, that is the fraction of true positives. 
We determine the set of true positive constraints to be the subset of all `loop closure constraints` which are not violated by more than 20 cm or 1 ◦ when we compute (SPA). 
We see that while our `scan-to-submap matching` procedure produces false positives which have to be handled in the optimization (SPA), it manages to provide a sufficient number of `loop closure constraints` in all test cases. 
Our use of the Huber loss in (SPA) is one of the factors that renders loop closure robust to outliers. 
In the Freiburg hospital case, the choice of a low resolution and a low minimum score for the `loop closure detection` produces a comparatively high rate of false positives. 
The precision can be improved by raising the minimum score for `loop closure detection`, but this decreases the solution quality in some dimensions according to `ground truth`. 
The authors believe that the `ground truth` remains the better benchmark of final map quality.

由于我们在Submap和扫描之间添加了`＂闭环＂约束`，因此数据集中不包含`基础事实`。
将数字与基于`scan-to-scan`的其他方法进行比较也很困难。
表IV显示了为每个测试用例添加的`＂闭环＂约束`的数量（真和假阳性），以及精度，即真阳性的分数。
我们确定真正的正约束集合是所有`＂闭环＂约束`的子集，当我们计算（SPA）时，它们不会超过20厘米或1秒。
我们看到，虽然我们的扫描到Submap匹配过程产生必须在优化（SPA）中处理的误报，但它设法在所有测试用例中提供足够数量的`＂闭环＂约束`。
我们在（SPA）中使用Huber损失是使＂闭环＂对异常值具有鲁棒性的因素之一。
在弗莱堡医院案例中，对闭环检测的低分辨率和低最低分数的选择产生相对较高的误报率。
通过提高闭环检测的最小分数可以提高精度，但是根据`基础事实`，这会降低某些维度的解决方案质量。
作者认为，`基础事实`仍然是最终地图质量的更好基准。

The parameters of Cartographer’s SLAM were not tuned for CPU performance. 
We still provide the wall clock times in Table V which were again measured on a workstation with an Intel Xeon E5-1650 at 3.2 GHz. 
We provide the duration of the sensor data for comparison.

Cartographer的SLAM参数没有针对CPU性能进行调整。
我们仍然提供表V中的挂钟时间，这些时间再次在具有3.2 GHz的Intel Xeon E5-1650的工作站上测量。
我们提供传感器数据的持续时间以供比较。

## VII. CONCLUSIONS 结论

In this paper, we presented and experimentally validated a 2D SLAM system that combines `scan-to-submap matching` with `loop closure detection` and `graph optimization`. 
Individual submap trajectories are created using our local, grid-based SLAM approach. 
In the background, all scans are matched to nearby submaps using `pixel-accurate `scan matching`` to create `loop closure constraints`. 
The constraint graph of submap and scan poses is periodically optimized in the background. 
The operator is presented with an upto-date preview of the final map as a GPU-accelerated combination of finished submaps and the current submap.
We demonstrated that it is possible to run our algorithms on modest hardware in real-time.

在本文中，我们提出并实验验证了一个2D SLAM系统，该系统将`扫描到Submap匹配`与`＂闭环＂检测`和`图形优化`相结合。
使用我们的基于网格的局部SLAM方法创建单个Submap轨迹。
在后台，所有扫描都使用`像素精确Scan match`匹配到附近的Submap，以创建`＂闭环＂约束`。
Submap和扫描位姿的约束图在后台定期优化。
向操作员呈现最终地图的最新预览，作为完成的子地图和当前子地图的GPU加速组合。
我们证明了可以在适度的硬件上实时运行我们的算法。

## ACKNOWLEDGMENTS 致谢

This research has been validated through experiments in the Deutsches Museum, Munich. 
The authors thank its administration for supporting our work. 
Comparisons were done using manually verified relations and results from [21] which uses data from the Robotics Data Set Repository (Radish) [19]. 
Thanks go to Patrick Beeson, Dieter Fox, Dirk Hahnel, Mike Bosse, John Leonard, ¨ Cyrill Stachniss for providing this data. 
The data for the Freiburg University Hospital was provided by Bastian Steder, Rainer Kummerle, Christian Dornhege, Michael Ruhnke, ¨ Cyrill Stachniss, Giorgio Grisetti, and Alexander Kleiner.

这项研究已通过慕尼黑德意志博物馆的实验得到验证。
作者感谢其政府支持我们的工作。
使用手动验证的关系和来自[21]的结果进行比较，该结果使用来自机器人数据集库（Radish）[19]的数据。
感谢Patrick Beeson，Dieter Fox，Dirk Hahnel，Mike Bosse，John Leonard，Cyrill Stachniss提供这些数据。
弗赖堡大学医院的数据由Bastian Steder，Rainer Kummerle，Christian Dornhege，Michael Ruhnke，Cyrill Stachniss，Giorgio Grisetti和Alexander Kleiner提供。

## REFERENCES 参考

[1] E. Olson, `M3RSM: Many-to-many multi-resolution `scan matching`,` in Proceedings of the IEEE International Conference on Robotics and Automation (ICRA), June 2015.
[2] K. Konolige, G. Grisetti, R. Kummerle, W. Burgard, B. Limketkai, ¨ and R. Vincent, `Sparse pose adjustment for 2D mapping,` in IROS, Taipei, Taiwan, 10/2010 2010.
[3] F. Lu and E. Milios, `Globally consistent range scan alignment for environment mapping,` Autonomous robots, vol. 4, no. 4, pp. 333– 349, 1997.
[4] F. Mart´ın, R. Triebel, L. Moreno, and R. Siegwart, `Two different tools for three-dimensional mapping: DE-based `scan matching` and feature-based loop detection,` Robotica, vol. 32, no. 01, pp. 19–41, 2014.
[5] S. Kohlbrecher, J. Meyer, O. von Stryk, and U. Klingauf, `A flexible and scalable SLAM system with full 3D motion estimation,` in Proc. IEEE International Symposium on Safety, Security and Rescue Robotics (SSRR). IEEE, November 2011.
[6] M. Himstedt, J. Frost, S. Hellbach, H.-J. Bohme, and E. Maehle, ¨ `Large scale place recognition in 2D LIDAR scans using geometrical landmark relations,` in Intelligent Robots and Systems (IROS 2014), 2014 IEEE/RSJ International Conference on. IEEE, 2014, pp. 5030– 5035.
[7] K. Granstrom, T. B. Sch ¨ on, J. I. Nieto, and F. T. Ramos, `Learning to ¨ close loops from range data,` The International Journal of Robotics Research, vol. 30, no. 14, pp. 1728–1754, 2011.
[8] G. Grisetti, C. Stachniss, and W. Burgard, `Improving grid-based SLAM with Rao-Blackwellized particle filters by adaptive proposals and selective resampling,` in Robotics and Automation, 2005. ICRA 2005. Proceedings of the 2005 IEEE International Conference on. IEEE, 2005, pp. 2432–2437.
[9] G. D. Tipaldi, M. Braun, and K. O. Arras, `FLIRT: Interest regions for 2D range data with applications to robot navigation,` in Experimental Robotics. Springer, 2014, pp. 695–710.


1875/5000
[1] E. Olson，`M3RSM：多对多分辨率Scan match`，载于IEEE国际机器人与自动化会议论文集（ICRA），2015年6月。
[2] K. Konolige，G。Grisetti，R。Kummerle，W。Burgard，B。Limketkai，¨和R. Vincent，`"稀疏位姿调整"2D绘图`，在IROS，台湾台北，2010年10月10日。
[3] F. Lu和E. Milios，`用于环境绘图的全局一致范围扫描对准`，自主机器人，第一卷。 4，不。 4，pp.333- 349,1997。
[4]F.Mart'ın，R。Triebel，L。Moreno和R. Siegwart，`两种不同的三维构图工具：基于DE的Scan match和基于特征的环路检测`，Robotica，vol。 32，不。 01，pp.19-41,2014。
[5] S. Kohlbrecher，J。Meyer，O。von Stryk和U. Klingauf，`具有完整3D运动估计的灵活且可扩展的SLAM系统`，Proc。 IEEE国际安全，安全和救援机器人研讨会（SSRR）。 IEEE，2011年11月。
[6] M. Himstedt，J。Frost，S。Hellbach，H.-J。 Bohme和E. Maehle，`使用几何地标关系的2D LIDAR扫描中的大规模地点识别`，智能机器人和系统（IROS 2014），2014年IEEE / RSJ国际会议。 IEEE，2014，pp.5030-5035。
[7] K. Granstrom，T。B.Sch¨on，J.I。Nieto和F. T. Ramos，`学习close闭合范围数据循环`，`国际机器人研究杂志`，第一卷。 30，不。 14，pp.1728-1754,2011。
[8] G. Grisetti，C。Stachniss和W. Burgard，`通过自适应提议和选择性重采样改进基于网格的SLAM与Rao-Blackwellized粒子滤波器`，机器人与自动化，2005年.ICRA 2005. 2005年会议记录IEEE国际会议。 IEEE，2005，pp.2432-2437。
[9] G. D. Tipaldi，M。Braun和K. O. Arras，`FLIRT：2D范围数据的兴趣区域，应用于机器人导航`，在实验机器人中。 Springer，2014年，第695-710页。