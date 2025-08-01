# PySparq 量子计算教程 - 控制门操作

## 控制门基础概念

### 控制门机制
控制门在基本量子操作的基础上增加执行条件：
- 当控制条件满足时执行目标操作
- 经典示例：CNOT门（当控制位为1时执行X门操作）

### 核心实现原理
```python
# 基础写法分解
cnot = Xgate_Bool(target_reg, target_bit)\\
       .conditioned_by_bit(control_reg, control_bit)
cnot(state)

# 链式调用简写
Xgate_Bool(r2, 0).conditioned_by_bit(r1, 0)(state)
```

## 控制条件类型

### 条件控制方法一览
| 方法名称                     | 功能描述                               | 参数格式                       |
|------------------------------|----------------------------------------|--------------------------------|
| `conditioned_by_bit`         | 单/多比特控制（指定bit位置）          | (寄存器, 位序) 或 [(寄存器,位序),...] |
| `conditioned_by_all_ones`    | 全1控制（寄存器所有bit必须为1）       | 寄存器ID 或 [寄存器ID,...]     |
| `conditioned_by_nonzeros`    | 非零控制（寄存器整体值不为0）         | 寄存器ID 或 [寄存器ID,...]     |
| `conditioned_by_value`       | 数值匹配控制（寄存器值等于指定值）    | (寄存器ID, 数值) 或 [(寄存器ID,数值),...] |

## 实践案例

### 系统初始化
```python
import pysparq as spq

state = spq.SparseState()
r1 = spq.AddRegister(name='reg1', type=spq.UnsignedInteger, size=4)(state)
r2 = spq.AddRegister(name='reg2', type=spq.UnsignedInteger, size=3)(state)

# 初始态准备
spq.Hadamard_Int_Full(r1)(state)
```

### 基础CNOT门操作
```python
# 当reg1[0]=1时，对reg2[0]执行X门
spq.Xgate_Bool(r2, 0).conditioned_by_bit(r1, 0)(state)
```

#### 执行结果特征

reg1值（二进制末位） | reg2值（二进制末位）
------------------|-------------------
0（偶数）          | 保持原值（0）
1（奇数）          | 翻转（0→1）

### 多重条件控制示例
```python
# 组合条件：当reg1[0]=1且reg2=5时，执行X门
spq.Xgate_Bool(r2, 1)\\
   .conditioned_by_bit(r1, 0)\\
   .conditioned_by_value(r2, 5)(state)
```

## 控制门运行结果解析

### 典型输出示例
```text
StatePrint (mode=Detail)
|(0)reg1 : UInt4 | |(1)reg2 : UInt3 |
0.250000+0.000000i  reg1=|0> reg2=|0>
0.250000+0.000000i  reg1=|1> reg2=|1>
...（交替模式持续出现）...
0.250000+0.000000i  reg1=|15> reg2=|1>
```

### 结果模式解读
- reg1的奇偶性决定reg2的末位状态
- 所有reg1值为奇数的基矢（末位为1）对应的reg2末位翻转为1
- 振幅保持不变

## 注意事项

### 重要使用规则
1. **不允许条件叠加**：
   ```python
   # 错误写法（多次叠加单个条件）
   op.conditioned_by_bit(r1,0).conditioned_by_bit(r2,1)

   # 正确写法（使用列表参数）
   op.conditioned_by_bit([(r1,0), (r2,1)])
   ```

2. **允许混合条件类型**：
   ```python
   # 允许不同类型条件混合
   op.conditioned_by_bit(r1,0)\\
     .conditioned_by_value(r2,5)
   ```

3. **控制顺序无影响**：
   ```python
   # 以下两种写法等效
   op.conditioned_by_bit(r1,0).conditioned_by_value(r2,5)
   op.conditioned_by_value(r2,5).conditioned_by_bit(r1,0)
   ```

### 性能优化建议
- 优先使用寄存器级条件（`conditioned_by_value`）而非逐比特判断
- 对大型系统尽量合并同类控制条件
- 避免在循环中动态创建控制条件
