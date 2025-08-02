# PySparq 量子计算教程 - 量子态与基本量子门

## 量子态与量子寄存器

### SparseState 对象
量子态在 PySparq 中表示为 `SparseState` 对象，包含以下核心信息：
- 量子系统的全部状态信息
- 量子寄存器的类型配置
- 各个量子态分量的振幅和基矢表示

### 添加量子寄存器
使用 `AddRegister` 方法添加量子寄存器：
```python
r1 = spq.AddRegister(
    name='reg1',          # 寄存器名称（字符串）
    type=spq.UnsignedInteger,  # 数据类型（见下文说明）
    size=4               # 量子比特数量（最多64）
)(state)                 # 作用到量子态对象
```

#### 数据类型说明
| 类型 | 说明 |
|------|------|
| `UnsignedInteger` | 无符号整数 |
| `SignedInteger`   | 有符号整数 |
| `General`         | 通用寄存器 |
| `FixedPoint`      | 定点数 |

> **数据类型的影响**：
> 1. 量子态显示格式
> 2. 保证量子操作的类型安全

## 量子门操作

### 基本使用流程
量子门操作分为两个阶段：
```python
# 阶段一：构造量子门
op = spq.Hadamard_Int_Full(r1)

# 阶段二：施加到量子态
op(state)

# 简写形式
spq.Hadamard_Int_Full(r1)(state)
```

### 常用量子门类型
| 门类型 | 作用说明 |
|--------|----------|
| `*_Int_Full` | 作用于寄存器的所有量子比特 |
| `*_Bool`     | 作用于单个量子比特 |

## 完整示例教程

### 初始化量子系统
```python
import pysparq as spq

# 创建初始量子态
state = spq.SparseState()

# 添加第一个寄存器
r1 = spq.AddRegister(
    name='reg1',
    type=spq.UnsignedInteger,
    size=4
)(state)

# 添加第二个寄存器
r2 = spq.AddRegister(
    name='reg2',
    type=spq.UnsignedInteger,
    size=3
)(state)
```

### 查看初始态
```python
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)
```
输出结果：
```
StatePrint (mode=Detail)
|(0)reg1 : UInt4 | |(1)reg2 : UInt3 | 
1.000000+0.000000i  reg1=|0> reg2=|0>
```

> 理论上：
> $$\ket{\psi_0}=\ket{0}_{\mathrm{reg1}} \otimes \ket{0}_{\mathrm{reg2}}$$

### 施加Hadamard门操作
```python
spq.Hadamard_Int_Full(r1)(state)
```
此时量子态展开为16个等幅分量：
```
0.250000+0.000000i  reg1=|0> reg2=|0>
0.250000+0.000000i  reg1=|1> reg2=|0>
...（共16个分量）...
0.250000+0.000000i  reg1=|14> reg2=|0>
0.250000+0.000000i  reg1=|15> reg2=|0>
```

> 理论上：
> 
>$$\begin{aligned}
\ket{\psi_1}&=H_{\mathrm{reg1}}^{\otimes 4}\ket{\psi_0}\\
&=\frac{1}{4}\sum_{i=0}^{15}\ket{i}_{\mathrm{reg1}}\otimes \ket{0}_{\mathrm{reg2}}
\end{aligned}$$




### 单比特门操作示例
```python
# X门作用于reg2的第0位
spq.Xgate_Bool(r2, 0)(state)

# Y门作用于reg2的第1位
spq.Ygate_Bool(r2, 1)(state)
```

最终量子态显示：
```
0.000000+0.250000i  reg1=|0> reg2=|3>
0.000000+0.250000i  reg1=|1> reg2=|3>
...（所有分量的reg2值变为3）...
0.000000+0.250000i  reg1=|14> reg2=|3>
0.000000+0.250000i  reg1=|15> reg2=|3>
```

> 理论上：
>
> $$\begin{aligned}
\ket{\psi_2}&=Y_{\mathrm{reg2}[1]}X_{\mathrm{reg2}[0]}\ket{\psi_1}\\
&=Y_{\mathrm{reg2}[1]} \frac{1}{4}\sum_{i=0}^{15}\ket{i}_{\mathrm{reg1}}\otimes \ket{0001}_{\mathrm{reg2}}\\
&=\frac{i}{4}\sum_{i=0}^{15}\ket{i}_{\mathrm{reg1}}\otimes \ket{0011}_{\mathrm{reg2}}
\end{aligned}$$
>
> 其中$X_{\mathrm{reg2}[0]}$表示作用在reg2寄存器的qubit 0上的X门操作，$Y_{\mathrm{reg2}[1]}$表示作用在reg2寄存器的qubit 1上的Y门操作。

