# 快速开始

本指南将帮助您快速安装 Qalgo 并运行您的第一个示例。

## 安装

### 系统需求

在安装之前，请确保您的系统满足以下要求：

-  **操作系统**：Windows、Linux 或 macOS。
-  **Python 版本**：需要 Python 3.10 或更高版本 (3.10+)。

### 安装方式

我们推荐使用 `pip` 从 PyPI 直接安装 Qalgo：

    pip install qalgo

## 使用示例

成功安装后，您可以尝试使用 Qalgo 的量子离散绝热算法（QDA）来求解一个简单的线性方程组 `Ax = b`。

    # 导入 qalgo 中的 qda 模块和 numpy
    from qalgo import qda
    import numpy as np

    # 定义线性方程组的系数矩阵 A
    # A = [[1, 2],
    #      [3, 5]]
    a = np.array([[1, 2], [3, 5]])

    # 定义常数向量 b
    b = np.array([1, 2])

    # 调用 qda.solve 函数求解
    # 该函数会返回方程组的解向量 x 的归一化结果
    x_hat = qda.solve(a, b)

    # 打印计算得到的解
    print("求解结果 x_hat:")
    print(x_hat)

