'''这一课我们将学习如何使用控制门。

控制门在基于普通的门/操作上，额外增加一定的条件

例如CNOT表示控制X门，即当控制比特为1时，目标比特做X门

在稀疏态模拟器中，我们先构造操作，再对它调用conditioned_by_....方法增加它的执行条件
'''

import pysparq as spq

state = spq.SparseState()

r1 = spq.AddRegister(name='reg1', type=spq.UnsignedInteger, size=4)(state)
r2 = spq.AddRegister(name='reg2', type=spq.UnsignedInteger, size=3)(state)

spq.Hadamard_Int_Full(r1)(state)

# 我们可以对reg1的最低一位比特和reg2的最低一位比特进行CNOT门操作
# 这个写法的解释是这样的：
# 首先CNOT门=X门+control qubit
# 所以CNOT(reg1[0], reg2[0]) = X(reg2[0])---control(reg1[0])
# 这里Xgate_Bool(reg2, 0)表示对reg2的第0位进行X门操作
# conditioned_by_bit(r1, 0)表示对reg1的第0位进行控制
spq.Xgate_Bool(r2, 0).conditioned_by_bit(r1, 0)(state)

# 打印量子态
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# 输出：
# StatePrint (mode=Detail)
# |(0)reg1 : UInt4 | |(1)reg2 : UInt3 |
# 0.250000+0.000000i  reg1=|0> reg2=|0>
# 0.250000+0.000000i  reg1=|1> reg2=|1>
# 0.250000+0.000000i  reg1=|2> reg2=|0>
# 0.250000+0.000000i  reg1=|3> reg2=|1>
# 0.250000+0.000000i  reg1=|4> reg2=|0>
# 0.250000+0.000000i  reg1=|5> reg2=|1>
# 0.250000+0.000000i  reg1=|6> reg2=|0>
# 0.250000+0.000000i  reg1=|7> reg2=|1>
# 0.250000+0.000000i  reg1=|8> reg2=|0>
# 0.250000+0.000000i  reg1=|9> reg2=|1>
# 0.250000+0.000000i  reg1=|10> reg2=|0>
# 0.250000+0.000000i  reg1=|11> reg2=|1>
# 0.250000+0.000000i  reg1=|12> reg2=|0>
# 0.250000+0.000000i  reg1=|13> reg2=|1>
# 0.250000+0.000000i  reg1=|14> reg2=|0>
# 0.250000+0.000000i  reg1=|15> reg2=|1>

# 可以看到reg1最低位是0的情况下（值是偶数），reg2也是0
# 而reg1最低位是1的情况下（值是奇数），reg2的最低位是1
# 这就是CNOT门的作用

# 所有的控制门都可以用这种方式进行构造
# 每个“可以被控制”的类（controllable）都注册了如下4个方法
# 1. conditioned_by_bit(self, reg: int, bit: int) -> self
# 表示对特定一个比特进行控制。输入还可以是list[Tuple[int, int]]，表示对多个比特进行控制。
# 2. conditioned_by_all_ones(self, reg: int) -> self
# 表示对特定一个寄存器进行全1控制。输入还可以是list[int]，表示对多个寄存器进行全1控制。
# 3. conditioned_by_nonzeros(self, reg: int) -> self
# 表示对特定一个寄存器进行非0控制（表示只要不是0则操作）。输入还可以是list[int]，表示对多个寄存器进行非0控制。
# 4. conditioned_by_value(self, reg: int, value: int) -> self
# 表示对特定一个寄存器进行特定值控制（等于该值则操作）。输入还可以是list[Tuple[int, int]]，表示对多个寄存器进行特定值控制。
# 注意：每个控制方法都各自只能执行一次，不支持重复执行。
# 例如 operation.condictioned_by_bit(reg1, 0).conditioned_by_bit(reg2, 1) 是不支持的，因为reg1已经被控制了。
# 但 operation.conditioned_by_bit([(reg1, 0), (reg2, 1)]) 是支持的
# 以及 operation.conditioned_by_bit(reg1, 0).conditioned_by_value(reg2, 1) 是支持的，因为reg2的特定值1可以被控制。