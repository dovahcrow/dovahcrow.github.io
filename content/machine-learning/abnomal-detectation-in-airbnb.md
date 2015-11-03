+++
date = "2015-11-03T10:36:23+08:00"
draft = true
title = "Airbnb支付系统的异常检测机制"
author = "danielglh"
+++

> 本文翻译自Airbnb工程师团队的这篇博客：http://nerds.airbnb.com/anomaly-detection/

我们迫切希望能为遍布全球的Airbnb房东和游客提供这样的完美支付体验：游客可以使用他们所熟悉的支付方式支付当地货币，而房东可以方便地选择自己偏好的货币来获得收入。例如，巴西的法定货币是巴西雷亚尔，当地人民所熟悉的支付方式则是Boleto。这与美国的现状大相径庭；可以想象，当这样的巨大差异存在于Airbnb服务的190个国家之间时，这个问题有多么复杂。

为了实现这个愿景，我们的[支付团队](http://nerds.airbnb.com/payments-airbnb/)搭建了一个安全、易用的世界级支付平台。团队的职责包括支持游客支付和房东提现的功能，一些全新的支付体验（例如[礼品卡](https://www.airbnb.com/gift)），以及财务核算协助等等。

由于Airbnb的业务遍布190个国家，我们就需要支持大量不同的货币和支付方式。大部分情况下，我们的系统运行无恙；但我们确实会遇到某些问题，例如某种货币无法支付，或者某个支付网关无法访问。为了在第一时间发现这些问题，数据科学团队开发了一套异常检测系统，能够在异常情况发生的时候实时定位问题所在。这套系统能够帮助产品团队迅速地发现问题和机遇；与此同时，数据科学家们有了更多的时间去做A/B测试（新的支付方式，新的产品发布），统计分析（价格对预订行为的影响，预测），以及建立机器学习模型来提供个性化的用户体验。

在本文中我会使用一些不同的模拟数据集来演示该模型是如何工作的，从而让你对我们开发的这套针对支付数据的异常检测工具有一个初步的了解。我们不妨假定当前时间为2020年的夏天，而我运营着一个网店并出售3种黑客外设：显示器，键盘和鼠标，有两家供应商：Lima和Hackberry为我的网店供货。

## 目的

这个异常检测系统的主要目的是要找到时间序列数据中的异常点。有些时候，我们大致看一下汇总数据就找到了；但大部分时候，我们需要深入分析数据并挖掘隐藏的趋势。我们来看一个例子，下图为显示器进货量的监测数据：

![显示器进货总量](http://nerds.airbnb.com/wp-content/uploads/2015/08/graph1.png)

显示器的进货数据总体看起来很正常。然后，我们来看一下两家供应商Lima和Hackberry的显示器进货数据分别是多少：

![显示器进货明细](http://nerds.airbnb.com/wp-content/uploads/2015/08/graph2.png)

我们可以看到，Lima作为我们的显示器主要供应商，从2020年的8月18号开始，连续3天无法供应足量的商品数量。在这段时间内，我们自动切换到次要供应商Hackberry作为主要货源。假如我们只是大致看一下汇总数据，就不可能发现这个问题，而对数据的深层次挖掘则能给我们提供信息去正确地定位问题所在。

## 模型

### 朴素回归模型

一种直观的构建模型的方式是简单地对标示一周中某一天的名义变量进行最小二乘法（[Ordinary Least Square, OLS](http://www.wikiwand.com/en/Ordinary_least_squares)）回归拟合。该模型可以用以下形式来表示：

$$y = at + b + \sum\_{i=1}^{7} a\_i*{I\_\textrm{day}}\_i + e$$

其中$y$是我们要追踪的数据，$t$是时间变量，${I\_\textrm{day}}\_i$是标示当天是否是一周中的第$i$天的指示变量，$e$则是误差项。这个模型比较简单，一般来说可以较好地识别趋势。但是它有几个缺点：

* 它对于数据增长的预测是线性的。如果我们的数据呈现指数级的增长，它就不适用于预测趋势。
* 它基于一个强假设——时间序列只是以一周为周期呈现季节性规律，因而无法处理具备其他季节性规律模式的产品。
* 太多的名义变量要求更大的样本数来保证回归系数达到所需要的显著性水平。

即便我们可以对我们想要追踪的数据模式进行观察，并且手动修正模型的表达式（比如我们观察到较强的以一个月或者一年为周期的季节性规律时，可以增加额外的名义变量），这是个无法扩展的过程。如果有一种方法可以自动识别季节性规律，就可以帮助我们消除偏见，并使我们可以把这项技术应用到支付领域之外的数据集。

### 快速傅里叶变换模型

当我们对时间序列进行趋势和季节性规律建模的时候，有一种通用做法是构建如下形式的模型：

$$Y = S + T + e$$

其中$Y$是度量值，$S$代表季节性规律，$T$代表趋势，$e$是误差项。例如，在我们的朴素回归模型中，$S$为指示函数的总和，而$T$则为$at+b$。

在下一节中，我们将利用上一节获取的知识，开发新的方法来检测趋势和季节性规律。我们将使用两种虚构的商品：键盘和鼠标的销量来演示该模型是如何工作的。两种商品的销售量如下图所示：

![键盘与鼠标的销量，2016年9月至2019年8月](http://nerds.airbnb.com/wp-content/uploads/2015/08/graph3.png)

如上所示，键盘是从2016年9月起售的主要商品，而鼠标从2017年8月才开始售卖。我们将会对季节性规律和趋势进行建模，并致力于找到那些误差大大偏离平均值的异常点。

## 季节性规律

我们使用快速傅里叶变换（[Fast Fourier Transform, FFT](http://www.wikiwand.com/en/Fast_Fourier_transform)）来检测季节性规律。在朴素线性回归模型中，我们假设销量具备以一周为周期的季节性规律。从上图我们可以看到，鼠标的销量并没有明显的以一周为周期的变化模式，因此盲目地假设这样的模式对我们的模型是不利的，只会无谓地增加名义变量。一般来说，如果我们有数量可观的历史数据，FFT可以作为检测季节性规律的好工具。将FFT应用到两组时间序列数据后，我们得到了如下图表：

![快速傅里叶变换曲线](http://nerds.airbnb.com/wp-content/uploads/2015/08/graph4.png)

其中season_day是变换后余弦波的周期。在FFT中，我们通常只选择有峰值振幅的周期来表征季节性，而将其他周期作为噪声处理。在这个例子中，我们观察到键盘数据有7和3.5两处较大的峰值，以及45和60两处较小的峰值。对于鼠标数据，我们观察到，在7天这一点上有显著的峰值，以及在35，60和80有一些较小的峰值。FFT生成的键盘和鼠标的季节性模式如下图所示：

![商品销量的季节性规律](http://nerds.airbnb.com/wp-content/uploads/2015/08/graph5.png)

我们可以看到，键盘的季节性振幅随着时间增大，并具备很强的以一周为周期的季节性模式，而鼠标则同时表现出非常强的以一周为周期和以40天为周期的季节性模式。

## 趋势

我们使用滚动中位数作为时间序列的趋势。这是基于在非常短的时间内，销量增长不会非常显著的假设。例如，对于特定的某一天，我们会用前7天的滚动中位数作为该天的趋势水平。使用中位数而不是平均数的好处在于在有极端数值的情况下更加稳定。例如，当我们在一两天中有十倍以上突然增长的时候，中位数并不会影响趋势水平，而平均值则会影响趋势水平。在这个示例中，我们使用14天的中位数作为趋势，如下图所示：

![商品销量的趋势](http://nerds.airbnb.com/wp-content/uploads/2015/08/graph6.png)

## 误差

得到季节性规律和趋势水平之后，我们来计算误差项。我们使用误差项来判定在时间序列数据中是否有异常点。当我们把趋势值和季节性规律组合在一起，然后从原始的销售数据中减去后，就得到了误差项，如下图所示：

![商品销量的误差项](http://nerds.airbnb.com/wp-content/uploads/2015/08/graph7.png)

我们可以看到，在误差项中有几个峰值代表了时间序列数据中的异常点。根据我们对假阳性（False Postive, FP）的容忍度，我们可以选择可以允许的以0为基准的标准差倍数。这里我们使用4倍标准差来得到较为合理的异常点数目，或者警报：

![键盘与鼠标销售数据的异常点](http://nerds.airbnb.com/wp-content/uploads/2015/08/graph8.png)

如上所示，警报系统较好地识别了误差项中的大多数峰值，这些峰值对应了数据中的一些异常点。我们注意到，有些检测到的异常点在人眼看来并不异常，但是考虑季节性变化规律的话，它们事实上的确是异常点。

总体来说，根据我们内部测试的结果，该模型在识别异常点上表现优异，同时对于数据作了最少的假设。

## 结论

本文提供了关于如何构建异常检测模型的一些观点。大多数异常检测模型包括了对季节性规律和趋势的模型构建。构建过程中一个关键因素是尽可能少地做假设，从而使模型具备足够的一般性，可以适用于更多情形；但是如果某些假设可以很好地简化你的模型，那也不妨一试。

*Translated by* **Daniel Gong**

Backend Engineer @ Strikingly.com