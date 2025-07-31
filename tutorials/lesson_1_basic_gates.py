'''这一课学习pysparq的量子态和基本量子门

量子态是一个SparseState对象，它包含了量子系统的全部信息，包括量子寄存器的类型和各个分量的振幅、基矢。

量子寄存器通过AddRegister方法进行添加，它决定了目前量子系统中有哪些量子比特。pysparq中可以定义多个量子寄存器，每个量子寄存器又可以定义多个量子比特。

在pysparq中，量子门or量子操作通常一个构造的对象，其中包含了门的类型、参数、作用对象等信息。

构造量子门之后，它需要作用在SparseState对象上，通过__call__方法调用
例如 

# step 1
op = spq.Hadamard_Int_Full(r0)
# 表示构造了一个作用在r0上的Hadamard门（Hadamard门是一种基本的量子门，Hadamard_Int_Full表示对量子寄存器的每个比特进行Hadamard门操作，后面会专门解释）

# step 2
op(state)
# 表示将刚才的操作作用在state上，这一步才真正的改变了state中的量子态

上述操作也可以写成一行代码
spq.Hadamard_Int_Full(r0)(state)

'''

import pysparq as spq

# 第一步，创建一个空的量子态
state = spq.SparseState()

# 之后，定义初始量子寄存器
# 
# 定义寄存器的名称、类型和大小，其中
#
# name（名字）：str，表示寄存器的名称
#
# type（类型）：spq.DataType，表示寄存器的类型，目前支持的类型有：
#     spq.UnsignedInteger：无符号整数
#     spq.SignedInteger：有符号整数
#     spq.General：一般寄存器，无类型
#     spq.FixedPoint：定点数
#     类型实际上并不影响计算，它只影响两个点：
#         a) 量子态在print的时候会以什么形式显示
#         b) 一些量子操作中可能会检查量子态的类型以保证运算安全
#
# size（大小）：int，表示寄存器的大小，即寄存器中量子比特的数量（最大64）
# 
# 这里定义的量子寄存器的名称为reg1，类型为无符号整数，大小为4
# 注意：AddRegister本身需要作用到state上与目前的量子态同步
r1 = spq.AddRegister(name='reg1', type=spq.UnsignedInteger, size=4)(state)

# 当然我们还可以继续定义多个寄存器
# 这里定义的量子寄存器的名称为reg2，类型为无符号整数，大小为3
r2 = spq.AddRegister(name='reg2', type=spq.UnsignedInteger, size=3)(state)

# 打印量子态
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# 输出：
# StatePrint (mode=Detail)
# |(0)reg1 : UInt4 | |(1)reg2 : UInt3 | 
# 1.000000+0.000000i  reg1=|0> reg2=|0>

# 我们可以看到，量子态中有两个寄存器，reg1和reg2，且都处于|0>态，量子态的振幅是1.0+0.0i

# 接下来，可以对量子态进行一定的操作
# 这里我们对reg1进行Hadamard门操作
spq.Hadamard_Int_Full(r1)(state)

# 打印量子态
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# 输出：
# StatePrint (mode=Detail)
# |(0)reg1 : UInt4 | |(1)reg2 : UInt3 |
# 0.250000+0.000000i  reg1=|0> reg2=|0>
# 0.250000+0.000000i  reg1=|1> reg2=|0>
# 0.250000+0.000000i  reg1=|2> reg2=|0>
# 0.250000+0.000000i  reg1=|3> reg2=|0>
# 0.250000+0.000000i  reg1=|4> reg2=|0>
# 0.250000+0.000000i  reg1=|5> reg2=|0>
# 0.250000+0.000000i  reg1=|6> reg2=|0>
# 0.250000+0.000000i  reg1=|7> reg2=|0>
# 0.250000+0.000000i  reg1=|8> reg2=|0>
# 0.250000+0.000000i  reg1=|9> reg2=|0>
# 0.250000+0.000000i  reg1=|10> reg2=|0>
# 0.250000+0.000000i  reg1=|11> reg2=|0>
# 0.250000+0.000000i  reg1=|12> reg2=|0>
# 0.250000+0.000000i  reg1=|13> reg2=|0>
# 0.250000+0.000000i  reg1=|14> reg2=|0>
# 0.250000+0.000000i  reg1=|15> reg2=|0>

# 此时我们就已经产生一个具有16个分量的量子态

# 接下来可以对reg2的最低一位比特做X门操作
spq.Xgate_Bool(r2, 0)(state)

spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# 输出：
# StatePrint (mode=Detail)
# |(0)reg1 : UInt4 | |(1)reg2 : UInt3 |
# 0.250000+0.000000i  reg1=|0> reg2=|1>
# 0.250000+0.000000i  reg1=|1> reg2=|1>
# 0.250000+0.000000i  reg1=|2> reg2=|1>
# 0.250000+0.000000i  reg1=|3> reg2=|1>
# 0.250000+0.000000i  reg1=|4> reg2=|1>
# 0.250000+0.000000i  reg1=|5> reg2=|1>
# 0.250000+0.000000i  reg1=|6> reg2=|1>
# 0.250000+0.000000i  reg1=|7> reg2=|1>
# 0.250000+0.000000i  reg1=|8> reg2=|1>
# 0.250000+0.000000i  reg1=|9> reg2=|1>
# 0.250000+0.000000i  reg1=|10> reg2=|1>
# 0.250000+0.000000i  reg1=|11> reg2=|1>
# 0.250000+0.000000i  reg1=|12> reg2=|1>
# 0.250000+0.000000i  reg1=|13> reg2=|1>
# 0.250000+0.000000i  reg1=|14> reg2=|1>
# 0.250000+0.000000i  reg1=|15> reg2=|1>

# 接下来对reg2的第1位比特做Y操作
spq.Ygate_Bool(r2, 1)(state)

spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# 输出：
# StatePrint (mode=Detail)
# |(0)reg1 : UInt4 | |(1)reg2 : UInt3 |
# 0.000000+0.250000i  reg1=|0> reg2=|3>
# 0.000000+0.250000i  reg1=|1> reg2=|3>
# 0.000000+0.250000i  reg1=|2> reg2=|3>
# 0.000000+0.250000i  reg1=|3> reg2=|3>
# 0.000000+0.250000i  reg1=|4> reg2=|3>
# 0.000000+0.250000i  reg1=|5> reg2=|3>
# 0.000000+0.250000i  reg1=|6> reg2=|3>
# 0.000000+0.250000i  reg1=|7> reg2=|3>
# 0.000000+0.250000i  reg1=|8> reg2=|3>
# 0.000000+0.250000i  reg1=|9> reg2=|3>
# 0.000000+0.250000i  reg1=|10> reg2=|3>
# 0.000000+0.250000i  reg1=|11> reg2=|3>
# 0.000000+0.250000i  reg1=|12> reg2=|3>
# 0.000000+0.250000i  reg1=|13> reg2=|3>
# 0.000000+0.250000i  reg1=|14> reg2=|3>
# 0.000000+0.250000i  reg1=|15> reg2=|3>

# 基本的逻辑门操作就介绍到这里，更多的操作请参考文档