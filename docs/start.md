
# 快速开始

## 安装

### 系统需求

- 操作系统：Windows、Linux 或 macOS
- Python 版本：3.9+

### 安装方式

```python
pip install qalgo
```

## 使用示例


```python
from qalgo import qda
import numpy as np

a = np.array([[1, 2], [3, 5]])
b = np.array([1, 2])
x_hat = qda.solve(a, b)
print(x_hat)
```

