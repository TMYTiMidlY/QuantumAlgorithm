# 欢迎使用 Qalgo

[![GitHub version](https://badge.fury.io/gh/tmytimidly%2Fquantumalgorithm.svg)](https://badge.fury.io/gh/tmytimidly%2Fquantumalgorithm)
[![Documentation Status](https://app.readthedocs.org/projects/qalgo/badge/?version=latest)](https://qalgo.readthedocs.io/zh-cn/latest/)
[![PyPI version](https://badge.fury.io/py/qalgo.svg)](https://badge.fury.io/py/qalgo)
[![Test status](https://github.com/TMYTiMidlY/QuantumAlgorithm/actions/workflows/tests.yml/badge.svg)](https://github.com/TMYTiMidlY/QuantumAlgorithm/actions/workflows/tests.yml)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qalgo)

这是 Quantum Algorithm (Qalgo) 项目的文档。

## 项目简介

Qalgo 是一个专注于量子算法实现与研究的 Python 工具库。本项目基于一个强大的后端量子虚拟机 [PySparQ](https://pypi.org/project/pysparq/) 实现，旨在为研究人员和开发者提供一系列模块化、易于使用且高性能的量子算法组件。

我们的目标是降低量子算法的学习与实践门槛，通过将复杂的量子算法封装为简洁的接口，加速量子计算在各个领域的应用探索。

## 核心依赖：PySparQ

Qalgo 的强大性能和灵活性离不开其核心依赖——**PySparQ**。PySparQ 是稀疏态模拟器 **SparQ** 的 Python 打包版本。SparQ 是一个由中国科学技术大学先进技术研究院（USTC-IAI）量子计算团队开发的高性能量子线路编程工具与模拟器。其关键特性包括：

- **稀疏量子态**：SparQ只处理量子态中振幅非0的部分
- **寄存器级**：SparQ对量子态的处理以**寄存器**为单位，从而允许在量子比特层面上进行扩展，在算术量子线路的计算上具有极高的便捷性。
- **可扩展性**：SparQ的架构设计上的自由度极高，可以根本性地优化特殊的量子线路的模拟。例如可以直接用FFT算法模拟QFT线路，从而取得比直接模拟QFT线路高得多的效率；或者直接利用算术运算来模拟量子算术运算线路，避免了将其拆解为基本门的繁琐过程。

Qalgo 充分利用了 PySparQ 的这些底层优势，为用户提供了更高层次的算法接口。

## 主要功能

本项目的能力分为两个层次：由 **PySparQ** 提供的底层组件和由 **Qalgo** 实现的上层算法。

### 由 PySparQ 提供的基础组件

PySparQ 为构建量子算法提供了丰富且高效的基础模块，包括：

-   量子逻辑门
-   量子算术运算
-   量子随机访问存储器 (QRAM)
-   量子傅里叶变换 (QFT)
-   量子态制备和量子测量


### Qalgo 算法库

Qalgo 利用 PySparQ 提供的强大组件，专注于实现完整的、端到端的量子算法。用户可以直接调用这些高层接口来解决具体问题。

#### 已实现

-   **[基于离散绝热定理的量子线性求解器](./algorithms/qda.md#algorithm-description)**

#### 待实现

我们计划在未来的版本中继续扩展算法库，包括但不限于：

-   Shor 算法
-   Grover 算法
-   哈密顿模拟
-   基于 HHL 算法的量子线性求解器