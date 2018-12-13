---
title: cartographer论文翻译 二维构图的高效稀疏位姿调整 
date: 2018-11-27 11:03:04
tags: 
- cartographer 
category: slam技术
mathjax: true
---
cartographer 论文翻译
<!-- more -->
## 摘要

位姿图已成为解决同时定位和构图（SLAM）问题的流行表示。
位姿图是一组机器人位姿，通过观察附近位姿共有的特征获得的非线性约束连接。
优化大型位姿图一直是移动机器人的瓶颈，因为直接非线性优化的计算时间可以随着图的大小而指数增长。
在本文中，我们提出了一种构造和求解线性子问题的有效方法，这是这些直接方法的瓶颈。
我们将我们称为稀疏位姿调整（SPA）的方法与竞争间接方法进行比较，并表明它在收敛速度和准确性方面优于它们。
我们在大量室内真实世界地图和非常大的模拟数据集上展示了它的有效性。
C++中的开源实现和数据集是公开可用的。

## 1. 介绍

机器人构图的最新文献显示出对基于图的SLAM方法的兴趣日益增加。
在最一般的形式中，图形具有表示机器人位姿和世界特征的节点，测量将它们连接为约束。
所有方法的目标是共同优化节点的位姿，以便最小化约束引入的误差。
该问题的一个经典变体来自计算机视觉，并表示为束调整[25]，其通常用Levenberg-Marquardt（LM）非线性优化器的专用变体解决。 
在SLAM文献中，Lu-Milios [18]，GraphSLAM [24]和√SAM[4]都是这种技术的变种。 


由于特征往往超过机器人位姿，
通过将特征观察转换为机器人位姿之间的直接约束，可以创建更紧凑的系统，
要么通过边缘化[1,24,4]，要么通过直接匹配 - 例如，
在两个机器人位姿之间匹配激光扫描产生两者的相对位姿估计。
在典型的机器人地图应用中，位姿约束系统表现出稀疏的连接结构， (所以SPA是通过位姿构造)
因为传感器的范围通常限于机器人的附近。

有效地解决位姿图（即，找到节点的最佳位置）是这些方法的关键问题，尤其是在在线构图问题的背景下。
100m x 100m 办公空间的典型2D激光地图可能有数千个节点和更多约束（见图1）。
此外，向此构图添加循环闭包约束可能会影响系统中的几乎所有位姿。
o
![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/f1.png)

LM方法的核心在于解决大的稀疏线性问题。

在本文中，我们开发了一种从约束图有效地计算稀疏矩阵的方法，并使用直接稀疏线性方法来解决它。
与视觉文献中的稀疏束调整类似，我们将此方法称为稀疏位姿调整（SPA），因为它处理位姿-位姿约束的受限情况。
SBA/GraphSLAM优化器与解决线性子问题的有效方法的组合具有以下优点。

* 它考虑约束中的协方差信息，从而得到更精确的解。

* SPA是健壮的并且容忍初始化，对于增量处理和批处理来说，具有非常低的故障率（陷入局部最小值）。

* 收敛非常快，因为它只需要LM方法的几次迭代。

* 与EKF和信息滤波器不同，SPA是完全非线性的：在每次迭代中，它线性化当前位姿周围的所有约束。

* SPA在批处理和增量模式下都是有效的

我们在实验结果部分记录了该方法的这些和其他特征，其中我们还将此方法与其他LM和非LM的最新优化器进行比较。

SPA效率的好处之一是，构图系统可以连续优化其图，提供所有节点的最佳全局估计，而计算开销非常小。
解决图1所示的大型地图的优化问题只需要距离里程计提供的初始配置150ms。

在增量模式下，在添加每个节点之后优化图，对于任何节点添加，它需要小于15ms。

尽管SPA可以用3D位姿参数化，但是本文将其局限于二维构图，这是一个具有多种竞争优化技术的成熟领域。
我们的意图是表明一个基于二维位姿的构图系统可以在线使用SPA作为其优化引擎，甚至在大规模环境和具有大环路闭合，而不诉诸子构图或复杂的划分方案。

## II. 相关工作

18 1997 -- 提出graph slam,无优化，慢

13 2001 -- 松弛法定位机器人
06 2002 -- 高斯-塞德尔松弛法最小化约束网络中的误差。
09 2005 -- 多层松弛法

21 2006 -- 优化位姿图 提出随机梯度下降法
10 2009 -- 基于树的参数化 提高梯度下降法收敛速度

02 1995 -- 最直观的方法:非线性最小二乘优化(ML pass) 一种有前途的技术是预条件共轭梯度PCG
15 2004 -- 大规模制图 使用了PCG作为解析器
20 2004 -- 大规模3d制图 使用了PCG作为解析器
05 1994 -- 稀疏矩阵库
03 2006 -- 直接线性求解器
04 2005 -- 使用稀疏的直接线性求解器[3]实现束调整
14 2007 -- $\sqrt{SAM}$的变体，称为iSAM

07 2006 -- 用信息矩阵形式递增地求解图的滤波技术:延迟稀疏信息滤波器（DSIF）
08 2006 -- 通过树表示来捕获系统的稀疏结构

00 2010 -- 直接稀疏Cholesky分解求解线性系统的二维位姿图优化方法

Lu和Milios[18]提出了基于图的SLAM的具有开创性的工作，其中他们通过ICP扫描匹配来确定扫描之间的成对测量，然后通过迭代线性化来优化该图。
那时，SLAM社区还没有有效的优化算法，基于图的方法被认为太耗时。
尽管如此，基于图的SLAM的直观公式吸引了许多研究者，并做出了有价值的贡献。

自从Lu和Milios论文发表以来，人们提出了许多图优化的方法。
霍华德等人[13]应用松弛法定位机器人并建立地图。
杜克特等人[6]提出了利用高斯-塞德尔松弛来最小化约束网络中的误差。
为了克服松弛法固有的收敛速度慢，Frase等人[9]提出了Gauss-Seidel松弛的一种变型，称为多层松弛法(MLR)。
它适用于不同分辨率的松弛。
据报道，MLR在2D环境中提供非常好的结果，尤其是在初始猜测的误差有限的情况下。

奥尔森[21]等人提出了随机梯度下降法来优化位姿图。
这种方法的优点是易于实现，并且对错误的初始猜测异常健壮。
后来，格里塞蒂等[10]通过应用显著提高收敛速度的基于树的参数化来扩展这种方法。
这些方法的主要问题是，它们假设图中的误差或多或少是均匀的，因此它们很难应用于某些约束未被指定的图。

优化图的最直观的方法可能是通过非线性最小二乘优化，如LM。
最小二乘法需要重复求解通过线性化图的原始似然函数而获得的大型线性系统。
这种线性系统通常非常大；因此，第一种基于图的方法是耗时的，因为它们没有利用其自然的稀疏性。
一种有前途的技术是预条件共轭梯度（PCG）[2]，后来被Konolige[15]和Montemerlo和Srun[20]用作大型稀疏位姿约束系统的有效求解器； 预条件通常是不完全Cholesky分解。
PCG是一种迭代方法，一般需要n次迭代才能收敛，其中n是图中变量的数目。
我们从Sparselib++和IML++[5]中实现了PCG的稀疏矩阵版本，并将该实现用于比较实验。

最近，Dellaert和他的同事使用束调整，他们使用稀疏的直接线性求解器[3]实现束调整；他们称他们的系统$\sqrt{SAM}$[4]。
我们的方法与SAM类似；主要在工程上不同，我们是通过使用有序数据结构高效地构造线性子问题。
我们还使用LM代替标准的非线性最小二乘法，从而提高了鲁棒性。
最后，我们介绍了增量情况下的一种“连续LM”方法，以及一种更稳健的批处理问题的初始化方法。

凯斯等人。[14]引入了$\sqrt{SAM}$的变体，称为iSAM，其执行与非线性最小二乘问题相关联的线性矩阵的增量更新。
只偶尔执行重线性化和变量排序，从而提高计算效率。
在我们的方法中，重新线性化和矩阵构造是非常有效的，因此这些方法变得不太必要。
目前，我们没有iSAM或_SAM的实现，无法针对性能进行测试。

松弛法或最小二乘法通过迭代地细化初始猜测来进行。
相反，基于随机梯度下降的方法对初始猜测更稳健。
在SLAM文献中，这种初始猜测的重要性经常被低估。
初始猜测越好，算法找到正确解决方案的可能性就越大。
在本文中，我们讨论了这一点，并评估了三种不同的策略来计算初始猜测。

与全非线性优化相比，一些研究人员探索了使用信息矩阵形式递增地求解图的滤波技术。
第一种这样的方法是由EuStruts等人提出的。
并称之为延迟稀疏信息滤波器（DSIF）〔7〕。
这种技术可能是非常有效的，因为它仅向系统信息矩阵添加少量的常数元素，甚至对于循环闭合也是如此。
然而，恢复所有节点的全局位姿需要求解一个大型的稀疏线性系统；有更快的方法来获得近似的最近位姿。

Frese提出了TreeMap [8]算法，该算法通过树表示来捕获系统的稀疏结构。
树中的每个叶子都是一个局部地图，估计的一致性是通过树发送更新到局部地图来实现的。
在理想条件下，此方法可以在O（n log n）时间内更新整个地图，其中n是地图中元素的数量。
但是，如果地图具有许多局部连接，则局部地图的大小可能非常大，并且它们的更新（被视为基本操作）变得计算成本昂贵，如本文其余部分所示。

综上所述，本文提出了一种利用直接稀疏Cholesky分解求解线性系统的二维位姿图优化方法。
线性系统的计算采用内存高效的方式，使缓存遗漏最小化，从而显著提高了性能。
我们将我们的方法在精度和速度上与可用的现有LM和非LM方法进行比较，并且表明SPA优于它们。
开源实现在C++和Matlab/OcthVE中都是可用的。
用于求解稀疏系统的有效直接（非迭代）算法已经变得可用[3]，从而恢复了一系列用于优化过去被丢弃的图的方法。

在本文中，

## III. SYSTEM FORMULATION

解决SLAM问题的流行方法是所谓的“基于图”或“基于网络”方法。
这个想法是通过图来表示机器人测量的历史。
图中的每个节点表示传感器测量或局部地图，并且用测量所处的位置对其进行标记。
两个节点之间的边缘编码由于连接测量的对齐而产生的空间信息，并且可以被视为两个节点之间的空间约束。

在基于图的SLAM环境中，通常考虑两个不同的问题。
第一种是基于传感器数据识别约束。
由于环境中的潜在模糊或对称性，这种所谓的数据关联问题通常很难解决。
这个问题的解决方案通常被称为SLAM前端，它直接处理传感器数据。
第二个问题是修正机器人的位姿，以获得给定约束环境的一致构图。
这种方法的这一部分通常被称为优化器或SLAM后端。
它的任务是寻找使约束中编码的测量的可能性最大化的节点的配置。
对这个问题的另一种观点是由物理学中的弹性模型给出的。
在这种观点中，节点被视为质量，而约束则被视为与质量相连的弹簧。
弹簧和质量的最小能量配置描述了构图问题的解决方案。

在其操作期间，基于图的SLAM系统交错前端和后端的执行，如图2所示。

![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/f2.png)

这是必需的，因为前端需要对部分优化的构图进行操作，以限制对潜在约束的搜索。
当前估计越精确，由前端生成的约束将越健壮，并且其操作也越快。
因此，从估计精度和执行时间方面衡量的优化算法的性能对整个构图系统有重要影响。

本文详细描述了一种高效紧凑的二维图优化方法。
我们的算法可以与处理不同类型传感器的任意前端耦合。
为了简洁的介绍，我们简短地描述了激光数据的前端。
然而，一般概念可以直接应用于不同的传感器。

## IV. SPARSE POSE ADJUSTMENT


为了优化一组位姿和约束，我们使用众所周知的Levenberg-Marquardt(LM)方法作为框架，并且使用特定的实现使其对于二维地图构建中遇到的稀疏系统有效。
类似于计算机视觉的稀疏束调整（SPA），它是用于相机和特征的LM的类似高效实现，我们称之为稀疏位姿调整（SPA）。

### A. Error Formulation

系统的变量是机器人的全局位姿集，通过平移和角度参数化:$c_i=[t_i , θ_i ] = [x_i , y_i , θ_i]^⊤$
约束是来自另一个（$c_i$）位置的一个节点$c_j$的测量。在$c_i$的帧中，$c_i$和$c_j$之间的测量偏移是$\overline{z}_{ij}$，具有精度矩阵Λij（协方差的倒数）。
对于$c_i$和$c_j$的任何实际位姿，它们的偏移可以计算为

![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/l1.png)

这里$R_i$是$θ_i$的2x2旋转矩阵。 $h(c_i , c_j )$称为测量方程。与约束相关的误差函数和总误差是

![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/l2.png)
    
注意，$h(c_i，c_j)$中的角度参数不是唯一的，因为加上或减去2π会产生相同的结果。当角度差发生时，它们总是标准化为间隔（-π，π）。

### B. Linear System

通过最小化等式2中的总误差来找到$c$的最佳位置。解决该问题的标准方法是Levenberg-Marquardt（LM），围绕c的当前值迭代线性化解。通过将变量c堆叠到向量x中来形成线性系统，并且误差函数被形成为向量e。然后我们定义：

![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/l3.png)

LM系统是:

![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/l4.png)

这里λ是一个小的正乘数，它在梯度下降和牛顿-欧拉方法之间转换。梯度下降更稳健，不太可能陷入局部最小值，但收敛缓慢;牛顿-欧拉的行为相反。通过为每个测量$h（c_i，c_j）$添加四个分量来形成矩阵H.

![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/l5.png)

这里我们略微滥用了J的符号，其中$J_i$是关于变量$c_i$的$e_{ij}$的雅可比行列式。这些组件都是3x3块。通过为每个约束添加3x1块$J_{c_i}Λ_{ij}e_{ij}$和$J_{c_j}Λ_{ij}e_{ij}$形成右侧。求解线性方程得到增量Δx即可被添加回x的当前值，如下所示：

![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/l6.png)

### C. Error Jacobians

测量函数的雅可比行列式在正则方程式（4）中出现，我们在这里列出它们。

![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/l7.png)

### D.  Sparsity 稀疏性

我们感兴趣的是大型系统，其中||c||的数量可以是10k或更多（我们能够找到的最大真实世界室内数据集是大约3k位姿，但我们可以生成任何顺序的合成数据集）。系统变量的数量是3||c||，而H矩阵是||c ||^2，或者超过$10^8$个元素。。操纵这样大的矩阵是昂贵的。幸运的是，对于典型的场景，约束的数量仅与位姿的数量成线性关系，因此它非常稀疏。我们可以利用稀疏性来更有效地解决线性问题。

为了以稀疏格式求解（4），我们使用CSparsepackage [3]。该软件包具有针对稀疏线性系统的高度优化的Choleskydecomposition求解器。它采用了几种高效分解策略，包括逻辑排序和近似最小度（AMD）算法，以便在变量很大时对变量进行重新排序。

通常，分解的复杂性将是变量数量的O（n3）。对于稀疏矩阵，复杂性将取决于Cholesky因子的密度，而Cholesky因子的密度又取决于H的结构及其变量的顺序。Mahon等[19]分析了Clesles分解的行为作为SLAM系统中闭环的函数。如果循环闭合的数量是恒定的，那么Cholesky因子密度是O（n），并且分解是O（n）。如果循环闭包的数量随着变量的数量线性增长，则Cholesky因子密度增长为O（n2），分解为O（n3）。

### E.  Compressed Column Storage 压缩列存储

LM算法的每次迭代都有三个步骤：建立线性系统、分解H和通过回代寻找$\Delta x$。建立系统的约束数量是线性的（因此基于多数图的SLAM系统的变量数量也是线性的）。在许多情况下，它可能成为线性求解器中成本较高的部分。这里我们概括了根据方程（5）产生的约束条件建立H的稀疏矩阵形式的一种有效方法。下图显示了基本思想。

CSparse使用压缩列存储（CCS）格式的forsparse矩阵。下图显示了基本概念。

![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/l8.png)

数组中的每个非零条目都放在val向量中。条目首先按列排序，然后按行排序。col_ptr每列有一个条目，加上最后一个条目，即非零总数（nnz）。列的col_ptr条目指向row_ind和val变量中列的开头。最后，row_ind给出了列中每个条目的行索引。

CCS格式具有存储效率，但难以逐步创建，因为对列的每个新的非零添加都会导致所有后续条目的移位。最有效的方法是按列顺序创建稀疏矩阵，这需要循环通过约束|| c ||次。相反，我们只修改一次约束，并将每个3x3块$J_i^TΛ_{ij}J_{i}$存储在一个与CCS格式平行的特殊的面向块的数据结构中。该算法在表I中给出。在该算法中，我们通过约束来将3×3块矩阵存储到C ++ std :: mapdata结构中，每列一个。构图在基于其键（行索引）的有序插入时是有效的。一旦创建了这个数据结构（步骤（2）），我们使用构图的有序特性来创建Hby的稀疏CCS格式，按照其键的顺序循环遍历每个构图，首先创建列和行索引，以及然后放入值。将列/行创建与值插入分开的原因是因为对于LM的任何迭代集合，前者只需要执行一次。

注意，只存储H的上三角形元素，因为CSparse中的Cholesky解算器仅查看该部分，并假设矩阵是对称的。

![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/t1.png)

F.可持续的LM系统

LM系统算法详见表II。对于具有相关测量的一组节点c，它在LM算法中执行一步。运行单次迭代允许LM的增量操作，以便在迭代之间可以添加更多节点。该算法是可持续的，因为λ在迭代之间被保存，因此连续迭代可以基于它们的结果改变λ。这个想法是添加一些节点和测量不会对系统产生太大的影响，因此λ的值具有关于梯度下降状态与欧拉 - 牛顿方法的信息。当发生循环闭合时，系统可能无法找到一个好的最小值，并且λ将在接下来的几次迭代中上升以使系统沿着良好的路径前进。

有许多不同的调整λ的方法;我们选择一个简单的方法。系统以一个小的lambda开始， $10^4$ 。如果更新的系统具有比原始系统更低的误差，则λ减半。如果误差相同或更大，则λ加倍。这在增量优化的情况下非常有效。只要在添加节点时误差减小，λ就会减小，系统会停留在Newton-Euler区域。当添加链接导致无法校正的大失真时，λ可以上升并且系统返回到更稳健的梯度下降。

## V.  SCAN MATCHING 扫描匹配

SPA需要通过激光扫描（或其他传感器）的匹配进行精确（逆协方差）估计。有几种扫描匹配算法可以提供这种算法，例如，Gutmannet等[11]使用点匹配参考扫描中提取的线，并返回高斯误差估计。最近，由Olson [22]扩展的Konolige和Chou [17]的相关方法提供了一种在给定范围内找到全局最佳匹配的有效方法，同时返回准确的协方差。该方法允许单个扫描或一组对齐扫描与另一个单个扫描或一组对齐扫描匹配。此方法在SRI的构图系统$Karto^1$中用于顺序扫描的局部匹配，以及[12]中的扫描集的循环闭包匹配。为了生成实验的真实数据集，我们在63个不同大小的存储机器人日志上运行Karto，使用其扫描匹配和优化器来构建构图并生成约束，包括循环闭包。保存图表并将其用作实验中所有方法的输入。

![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/t2.png)

## VI.  EXPERIMENT 实验

在本节中，我们将展示实验，其中我们将SPA与63个真实世界数据集和大型模拟数据集上的最新方法进行比较。我们考虑了各种各样的方法，包括最先进的技术。

* 信息过滤器：DSIF[7] 
* 随机梯度下降：环面[ 10 ]
* 分解非线性系统：Treemap[8]
* 稀疏姿态调整：SPA，带有(a)稀疏直接Cholesky求解器和(b)迭代PCG[15]

我们更新了PCG实现，以使用与SPA相同的“连续LM”方法；惟一的区别在于底层的线性求解器。先决条件是不完全Cholesky方法，共轭梯度以稀疏矩阵形式实现。我们还评估了一个稠密的Cholesky求解器，但是计算和内存需求都比其他方法大几个数量级。例如，对于具有1600个约束和800个节点的数据集，使用密集Cholesky求解器进行迭代需要2.1秒，而其他方法平均需要几毫秒。所有实验都在2.67Ghz运行的Intel Core i7-920上进行。

![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/f3.png)

在下文中，我们报告了在不同操作条件下方法的行为的累积分析；所有数据集的结果可在线查阅www.ros.org/./2010/spa。我们在批处理和在线两种模式下测试了各种方法。在批处理模式下，我们为算法提供全图，而在线模式下，每当向图中添加一个新节点时，我们都进行一定数量的迭代。在本节的其余部分中，我们首先讨论离线实验，然后介绍在线实验。通过对大规模仿真数据集上各种方法的分析，得出结论。

### A.精度测量

对于这些室内数据集，没有基本事实。相反，姿态约束系统的优良性度量是约束的协方差加权平方误差，或称^2误差。如果扫描匹配器是准确的，那么较低的^2表示扫描对齐得更好。图3显示了在真实世界数据集上的这种效果。

### B.真实世界实验：离线优化。

为了离线优化数据集，我们为每个优化器提供问题的完整描述。我们在比较DSIF和TreeMap时省略了它们，因为它们只增量地操作（DSIF相当于批处理模式下SPA的一次迭代）。由于离线优化的成功很大程度上取决于初始猜测，因此我们还研究了两种初始化策略，如下所述。

* 里程计: 图中的节点用增量约束进行初始化。这是几乎所有的图优化算法所采用的标准方法。
* 生成树: 使用广度优先访问在图上构造生成树。树的根是图的第一个节点。节点的位置根据生成树的深度优先访问进行初始化。将子节点的位置设置为根据连接约束转换后的父节点的位置。在我们的实验中，这种方法给出了最好的结果。

![image](https://raw.githubusercontent.com/lsy563193/image/master/cartographer_notes/2d-spa/f4.png)

对于每个数据集和每个优化器，我们计算上面描述的初始猜测。每个优化器都运行最少的迭代次数，或者直到满足终止条件为止。我们测量了收敛所需的时间和每种方法的2误差。图4总结了Odo.和Spanning-Tree初始化的结果。对于这些数据集，这两种类型的初始化在性能上没有实质性差异。

在误差图中，PCG和SPA收敛到几乎完全相同的解，因为唯一的区别是线性差异。求解器。它们都主导TORO，对于较大的图，TORO的误差是TORO的10倍以上。我们把此归因于TORO无法处理非球面协方差，以及它的非常慢的收敛特性。对于几乎所有的图，SPA所需的计算量几乎比PCG或TORO少一个数量级。

TORO被设计成对糟糕的初始化具有鲁棒性，并且为了测试这一点，我们还运行所有方法，所有节点都初始化为(0，0，0)。在这种情况下，SPA和PCG收敛到所有数据集的非全局最小值，而TORO能够重建正确的拓扑。

### C.真实世界实验：在线优化

对于在线比较，我们通过添加一个节点以及通过将新添加的节点连接到先前存在的图来递增地扩充图。我们在插入每个节点之后调用优化器，并且以这种方式在与SLAM前端一起执行时模拟它的行为。对于最大次数的迭代，或者直到误差不减小为止，进行优化。SPA/PCG的最大迭代次数是1；TreeMap为3；TORO为100。由于PCG迭代求解线性子问题，因此我们把其限制在50次迭代。选择这些阈值是为了在减少错误方面获得最佳性能。


在收敛性方面，SPA/PCG方法占主导地位。这对于DSIF的情况并不奇怪，DSIF是一种信息过滤器，因此在关闭大循环时会出现线性化误差。TORO具有与SPA最接近的性能，但每次迭代的收敛速度非常慢，这是梯度方法的特点；在收敛性方面，SPA/PCG方法占主导地位。这对于DSIF的情况并不奇怪，DSIF是一种信息过滤器，因此在关闭大循环时会出现线性化误差。TORO算法与SPA算法性能最接近，但每次迭代的收敛速度很慢，具有梯度法的特点；在收敛性方面，SPA/PCG算法是其他算法的主要特点。这对于DSIF的情况并不奇怪，DSIF是一种信息过滤器，因此在关闭大循环时会出现线性化误差。TORO具有与SPA最接近的性能，但每次迭代的收敛速度非常慢，这是梯度方法的特点；它也不处理非循环协方差，这限制了它实现最小2的能力。由于树图具有建立树结构进行优化的复杂策略，因此很难进行分析。对于这些数据集，它似乎有一个带有小叶子的大树（大型数据集循环）。通过固定线性化和删除连接，优化了树结构，使计算速度快，但收敛性差，2比SPA差近3个数量级。

所有的方法在约束图的大小上都是近似线性的，这意味着大循环闭包的数量增长缓慢。在所有数据集中，Treemap的性能最好，其次是SPA和DSIF。注意，SPA的行为是极其规则的：在任何数据集上与线性级数几乎没有偏差。此外，平均时间和最大时间是相同的：参见图8中的图表。最后，TORO和PCG每次迭代使用更多的时间，PCG大约是SPA的四倍。由于SPA的快速收敛性，我们只需每增加n个节点，就可以实现更低的计算量。我们强调这些图表是我们所能找到的最大的室内数据集，它们对SPA来说并不具有挑战性。

### D.合成数据集

为了估计算法的渐近行为，我们生成一个大的模拟数据集。机器人在网格上移动，网格的每个单元格都有5米的一边，我们每米创建一个节点。这个机器人的感知范围是1.5米。机器人的运动和测量都受到标准偏差为u=diag(0.01m,0.01m,0.5deg)的零均值高斯噪声的影响。每当机器人接近它访问过的位置时，我们就生成一个新的约束。模拟区域跨度超过500×500米，轨道总长100公里，重复观测频繁。全图如图6所示。这是一个极具挑战性的数据集，比任何真实世界的数据集都要糟糕。下面，我们报告所有我们比较的算法的批处理和在线执行的结果。

a)离线优化：每个批处理方法都使用前面部分描述的三个初始化来执行：里程计、生成树和零。结果如图7所示，是时间的函数。唯一能从零或里程表初始化优化图的方法是TORO；SPA/PCG在里程表或零开始时基本上不会收敛到全局最小值。SPA/PCG在生成树初始化后10秒左右全局收敛，在收敛点SPA明显更快（参见图7中的放大图）。TORO具有良好的初始收敛性，但由于梯度下降而具有长尾。

b)在线优化：我们增量地处理数据集，如第六-C节所述。在图8中，我们报告了每增加一个节点2误差和时间的演变。SPA和TreeMap都收敛到最小2（对于收敛图，参见图7）。然而，它们的计算行为非常不同：TreeMap每次迭代最多可以使用100秒，而SPA随着图的大小而缓慢增长。由于TreeMap在数据集中进行重访，因此树形图具有叶子非常大的小树，并且在每个叶子处执行LM优化，导致低误差和高计算量。其他方法具有与SPA等效的计算量，但不收敛。同样地，DSIF性能很差，并且不会收敛。TORO收敛，但是像往常一样难以清除小的误差。PCG的尖峰是由于它没有完全解决线性子问题，最终导致较高的整体误差。


## VII. 结论

本文提出并实验验证了一个二维姿态图的稀疏姿态调整非线性优化系统。SPA依赖于有效的线性矩阵构造和稀疏的非迭代Cholesky分解来有效地表示和解决大型稀疏姿态图。我们所能找到的真实数据集中没有一个是具有挑战性的——即使在批处理模式下也是如此。最大构图需要次秒的时间才能完全优化。联机计算最坏在10ms/节点范围内；与EKF滤波器或其他计算性能差的方法不同，我们不需要将构图分割成子构图[23]来获得全局最小误差。

与现有方法相比，SPA更快，收敛更好。唯一的例外是在初始化较差的构图中，只有TORO的随机梯度技术才能收敛；但是通过应用生成树初始化，SPA甚至能比TORO更好地解决复杂的合成实例。当与扫描匹配前端结合时，SPA将支持在线勘探和地图构建。因为SPA是一种姿态图方法，所以它允许对地图进行增量添加和删除，便于终身构图[16]。

用于运行SPA的所有相关代码和我们实现的其他方法都可以作为开放源码以及数据集和仿真生成器（www.ros）在线获得。org/./2010/spa)随附的视频显示在一个大型的真实世界数据集上的在线和离线模式下的SPA。


##  REFERENCES

[1]  M.  Agrawal  and  K.  Konolige.  FrameSLAM:  From  bundle  adjustmentto  real-time  visual  mapping.IEEE  Transactions  on  Robotics,  24(5) October 2008.

[2]   F. F. Campos and J. S. Rollett. Analysis of preconditioners for conjugategradients  through  distribution  of  eigenvalues.Int.  J.  of  ComputerMathematics, 58(3):135–158, 1995.

[3]   T. A. Davis.Direct Methods for Sparse Linear Systems (Fundamentalsof  Algorithms  2).Society  for  Industrial  and  Applied  Mathematics,Philadelphia, PA, USA, 2006.

[4]   F.  Dellaert.    Square  Root  SAM.    InProc.  of  Robotics:  Science  and Systems (RSS), pages 177–184, Cambridge, MA, USA, 2005.

[5]   J. Dongarra, A. Lumsdaine, R. Pozo, and K. Remington. A sparse matrixlibrary  in  c++  for  high  performance  architecture   s.  InObject OrientedNumerics Conference, pages 214–218, 1994.

[6]   T. Duckett, S. Marsland, and J. Shapiro. Fast, on-line learning of globally consistent maps.Journal of Autonomous Robots, 12(3):287 – 300, 2002.

[7]   R. M. Eustice, H. Singh, and J. J. Leonard. Exactly sparsedelayed-statefilters for view-based SLAM.IEEE Trans. Robotics, 22(6), 2006.

[8]   U.  Frese.    Treemap:  Ano(logn)algorithm  for  indoor  simultaneouslocalization  and  mapping.Journal of Autonomous Robots,  21(2):103–122, 2006.

[9]   U. Frese, P. Larsson, and T. Duckett.  A multilevel relaxation algorithmfor  simultaneous  localisation  and  mapping.IEEE  Transactions  onRobotics, 21(2):1–12, 2005.

[10]  G. Grisetti, C. Stachniss, and W. Burgard. Non-linear constraint networkoptimization for efficient map learning.IEEE Transactions on IntelligentTransportation Systems, 10:428–439, 2009.  ISSN: 1524-9050.

[11]  J.-S. Gutmann, M. Fukuchi, and K. Sabe. Environment identification bycomparing maps of landmarks. InInternational Conference on Roboticsand Automation, 2003.

[12]  J.-S.  Gutmann  and  K.  Konolige.   Incremental  mapping  of  large  cyclicenvironments.  InProc. of the IEEE Int. Symposium on ComputationalIntelligence in Robotics and Automation (CIRA), pages 318–325, Mon-terey, CA, USA, 1999.

[13]  A.  Howard,  M.  Matari ́c,  and  G.  Sukhatme.    Relaxation  on  a  mesh:a  formalism  for  generalized  localization.    InProc.  of  the  IEEE/RSJInt. Conf. on Intelligent Robots and Systems (IROS), pages 1055–1060,2001.

[14]  M.  Kaess,  A.  Ranganathan,  and  F.  Dellaert.   iSAM:  Fast  incrementalsmoothing and mapping with efficient data association.  InInternationalConference on Robotics and Automation, Rome, 2007.

[15]  K. Konolige.  Large-scale map-making.  InProceedings of the NationalConference on AI (AAAI), 2004.

[16]  K.  Konolige  and  J.  Bowman.Towards  lifelong  visual  maps.InInternational  Conference  on  Intelligent  Robots  and  Systems,  pages1156–1163, 2009.

[17]  K.  Konolige  and  K.  Chou.   Markov  localization  using  correlation.   InProc. of the Int. Conf. on Artificial Intelligence (IJCAI), 1999.

[18]  F.  Lu  and  E.  Milios.    Globally  consistent  range  scan  alignment  for environment mapping. Journal of Autonomous Robots, 4:333–349, 1997.

[19]  I. Mahon, S. Williams, O. Pizarro, and M. Johnson-Roberson.  Efficientview-based  SLAM  using  visual  loop  closures.IEEE  Transactions  onRobotics, 24(5):1002–1014, October 2008.

[20]  M. Montemerlo and S. Thrun. Large-scale robotic 3-d mapping of urbanstructures.  InISER, 2004.

[21]  E. Olson, J. Leonard, and S. Teller.  Fast iterative optimization of posegraphs  with  poor  initial  estimates.  InProc. of the IEEE Int. Conf. onRobotics & Automation (ICRA), pages 2262–2269, 2006.

[22]  E.  B.  Olson.    Real-time  correlative  scan  matching.    In International Conference on Robotics and Automation, pages 4387–4393, 2009.

[23]  L.  Paz,  J.  Tard ́os,  and  J.  Neira.   Divide  and  conquer:  EKF  SLAM  inO(n).IEEE Transactions on Robotics, 24(5), October 2008.

[24]  S.  Thrun  and  M.  Montemerlo. The  graph  SLAM  algorithm  with applications  to  large-scale  mapping  of  urban  structures.Int.  J.  Rob.Res., 25(5-6):403–429, 2006.

[25]  B. Triggs, P. F. McLauchlan, R. I. Hartley, and A. W. Fitzibbon. Bundle adjustment  -  a  modern  synthesis.   InVision  Algorithms:  Theory  and Practice, LNCS, pages 298–375. Springer Verlag, 2000.
