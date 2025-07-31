'''有时候我们想同时控制多个量子态

在pysparq中，我们只能让这些量子态共享量子寄存器的名字空间

比如不能拥有state1和state2，其中state1有3个寄存器，state2有2个寄存器

这表示AddRegister是全局化的。

如果我们想进行全新的计算，有两个选择：
1. 手动调用RemoveRegister删除所有寄存器
2. 调用spq.System.clear()清空整个系统
'''


import pysparq as spq

state = spq.SparseState()

r1 = spq.AddRegister(name='reg1', type=spq.UnsignedInteger, size=4)(state)
r2 = spq.AddRegister(name='reg2', type=spq.UnsignedInteger, size=3)(state)

# 打印量子态
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# 这里可以看到两个寄存器
# StatePrint (mode=Detail)
# |(0)reg1 : UInt4 | |(1)reg2 : UInt3 | 
# 1.000000+0.000000i  reg1=|0> reg2=|0>

spq.System.clear()

# 打印量子态
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# 这里就不再拥有寄存器了
# StatePrint (mode=Detail)

# 1.000000+0.000000i

r1 = spq.AddRegister(name='reg3', type=spq.UnsignedInteger, size=4)(state)

# 打印量子态
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# 目前就只有一个reg3
# StatePrint (mode=Detail)
# |(0)reg3 : UInt4 | 
# 1.000000+0.000000i  reg3=|0>