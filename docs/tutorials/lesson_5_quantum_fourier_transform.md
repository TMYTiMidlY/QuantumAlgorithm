# PySparq 量子计算教程 - 量子傅里叶变换

## 1. 量子傅里叶变换简介
量子傅里叶变换 (QFT) 是量子计算中最重要的算法之一，它将量子态从空间域转换到频率域，是 Shor 算法、量子相位估计等核心算法的关键步骤。pysparq 提供了一个简洁的 `QFT()` 操作符，可直接对寄存器执行 QFT。

---

## **2. 代码解析**
我们通过一个 4 比特寄存器的例子展示 QFT 的操作和相位影响：

```python
import pysparq as spq

state = spq.SparseState()
r1 = spq.AddRegister(name='reg1', type=spq.UnsignedInteger, size=4)(state)

# 步骤 1: 对 r1 应用全局哈达玛门（创建均匀叠加态）
spq.Hadamard_Int_Full(r1)(state)

# 步骤 2: 执行 QFT
spq.QFT(r1)(state)

# 打印初始量子态（均匀叠加态）
print("After QFT:")
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)
```

---

## **3. 预期输出与解释**
输出显示所有 16 个基态的概率幅均为 `0.25`：
```
StatePrint (mode=Detail)
|(0)reg1 : UInt4 | 
0.250000+0.000000i  reg1=|0>
0.250000+0.000000i  reg1=|1>
...
0.250000+0.000000i  reg1=|15>
```
**原理**:  
QFT 的数学定义为：
\[
\text{QFT}|x\rangle = \frac{1}{\sqrt{N}} \sum_{k=0}^{N-1} e^{2\pi i x k / N} |k\rangle
\]
对于初始的均匀叠加态 `|x⟩ = |+⟩⊗4`，QFT 的输出仍为均匀叠加态。这是因为 QFT 对均匀分布的输入具有对称性。

---

## **4. 相位操作的影响**
接下来，我们对寄存器的最低位（LSB）施加一个 `Z` 门：

```python
# 对最低位施加 Z 门（相位翻转）
spq.Zgate_Bool(r1, 0)(state)
print("After Z:")
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)
```

Z 门的作用是：
\[
Z|0\rangle = |0\rangle, \quad Z|1\rangle = -|1\rangle
\]
此时，`r1` 的最低有效位为 `1` 的基态（奇数）将获得一个 `-1` 的相位。

---

## **5. 逆量子傅里叶变换（IQFT）**
再次执行 QFT（实际为逆变换）以观察相位变化的影响：
```python
spq.QFT(r1)(state)
print("After Second QFT:")
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)
```

输出结果为：
```
StatePrint (mode=Detail)
|(0)reg1 : UInt4 | 
1.000000+0.000000i  reg1=|8>
```

---

## **6. 结果分析**
最终量子态坍缩到 `|8⟩`，这是因为：
1. **Z 门的作用**：  
   对最低位施加 Z 门后，所有奇数状态的振幅被翻转相位。此时的量子态为：
   \[
   |\psi\rangle = \frac{1}{4} \sum_{x=0}^{15} (-1)^{x_0} |x\rangle
   \]
   其中 \(x_0\) 是 \(x\) 的最低位。

2. **逆 QFT 的作用**：  
   第二次 QFT 实际上执行了逆变换（IQFT），将相位信息转换为位置信息。由于相位模式对应周期性信号，逆变换会将该模式映射到特定基态。

3. **结果 `|8⟩` 的解释**：  
   `8` 的二进制表示为 `1000`，对应量子寄存器最高位（MSB）为 `1`。这表明相位翻转影响了最高位的测量结果（周期性信号的频率检测）。

---

## **7. 关键概念总结**
- **QFT 与 IQFT 的关系**：  
  QFT 和 IQFT 互为逆操作。在 pysparq 中，`QFT()` 默认执行正向变换，若需要逆变换需显式调用 `QFT().dagger()`，但某些实现可能隐式处理相位反转。

- **相位敏感操作**：  
  量子算法（如 Shor 算法）利用相位翻转和干涉效应提取周期信息。本例展示了如何通过 Z 门和 QFT 的配合实现这一过程。

- **寄存器顺序问题**：  
  QFT 的实现依赖量子比特的顺序（通常为高位在前）。若寄存器定义顺序不同，结果可能对应不同基态。

---

## **8. 扩展实验**
尝试修改代码以观察不同行为：
1. **更改 Z 门的位置**：  
   对高位比特施加 Z 门（如 `spq.Zgate_Bool(r1, 3)`），观察结果是否变为 `|1⟩`。
   ```python
   spq.Zgate_Bool(r1, 3)(state)  # 影响最高位（第 3 位）
   ```

2. **多比特相位翻转**：  
   组合多个 Z 门观察干涉模式的叠加：
   ```python
   spq.Zgate_Bool(r1, 0)(state)
   spq.Zgate_Bool(r1, 2)(state)
   ```

---

通过本教程，读者可以掌握 pysparq 中量子傅里叶变换的操作方法，并理解相位操作对量子态的影响。这一技术是构建复杂量子算法（如因子分解、量子模拟）的基础。