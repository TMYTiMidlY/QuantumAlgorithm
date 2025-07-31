'''pysparq的一个特色就是可以在寄存器层面执行算术运算操作

这极大的简化了我们以往通过量子逻辑门编程算术运算的复杂度

并且pysparq提供的StatePrint功能可以很直观的去查看运算的结果的正确性

下面我们演示两种不同的量子加法，其中一个是对一个寄存器加一个常数，保存到第二个寄存器中，另一个是把两个寄存器的值相加，保存到第三个寄存器中

pysqarq原生支持大量算术运算操作，并且十分容易进行扩展
'''
import pysparq as spq

state = spq.SparseState()

# 定义3个4比特寄存器，每个寄存器的值都在0~15之间
r1 = spq.AddRegister(name='reg1', type=spq.UnsignedInteger, size=4)(state)
r2 = spq.AddRegister(name='reg2', type=spq.UnsignedInteger, size=4)(state)
r3 = spq.AddRegister(name='reg3', type=spq.UnsignedInteger, size=4)(state)

# 对r1使用Hadamard门
spq.Hadamard_Int_Full(r1)(state)

# 执行加法操作
# 这里对r1加一个常数，以r2为输出

spq.Add_UInt_ConstUInt(r1, 2, r2)(state)


# 打印量子态
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# |(0)reg1 : UInt4 | |(1)reg2 : UInt4 | |(2)reg3 : UInt4 | 
# 0.250000+0.000000i  reg1=|0> reg2=|2> reg3=|0>
# 0.250000+0.000000i  reg1=|1> reg2=|3> reg3=|0>
# 0.250000+0.000000i  reg1=|2> reg2=|4> reg3=|0>
# 0.250000+0.000000i  reg1=|3> reg2=|5> reg3=|0>
# 0.250000+0.000000i  reg1=|4> reg2=|6> reg3=|0>
# 0.250000+0.000000i  reg1=|5> reg2=|7> reg3=|0>
# 0.250000+0.000000i  reg1=|6> reg2=|8> reg3=|0>
# 0.250000+0.000000i  reg1=|7> reg2=|9> reg3=|0>
# 0.250000+0.000000i  reg1=|8> reg2=|10> reg3=|0>
# 0.250000+0.000000i  reg1=|9> reg2=|11> reg3=|0>
# 0.250000+0.000000i  reg1=|10> reg2=|12> reg3=|0>
# 0.250000+0.000000i  reg1=|11> reg2=|13> reg3=|0>
# 0.250000+0.000000i  reg1=|12> reg2=|14> reg3=|0>
# 0.250000+0.000000i  reg1=|13> reg2=|15> reg3=|0>
# 0.250000+0.000000i  reg1=|14> reg2=|0> reg3=|0>
# 0.250000+0.000000i  reg1=|15> reg2=|1> reg3=|0>

# 可以看到reg2保存了reg1的值+2的结果，并且针对位不够的部分进行了溢出处理。

# 进一步，我们可以将r1和r2加起来，保存到r3中

spq.Add_UInt_UInt(r1, r2, r3)(state)

# 打印量子态
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# StatePrint (mode=Detail)
# |(0)reg1 : UInt4 | |(1)reg2 : UInt4 | |(2)reg3 : UInt4 |
# 0.250000+0.000000i  reg1=|0> reg2=|2> reg3=|2>
# 0.250000+0.000000i  reg1=|1> reg2=|3> reg3=|4>
# 0.250000+0.000000i  reg1=|2> reg2=|4> reg3=|6>
# 0.250000+0.000000i  reg1=|3> reg2=|5> reg3=|8>
# 0.250000+0.000000i  reg1=|4> reg2=|6> reg3=|10>
# 0.250000+0.000000i  reg1=|5> reg2=|7> reg3=|12>
# 0.250000+0.000000i  reg1=|6> reg2=|8> reg3=|14>
# 0.250000+0.000000i  reg1=|7> reg2=|9> reg3=|0>
# 0.250000+0.000000i  reg1=|8> reg2=|10> reg3=|2>
# 0.250000+0.000000i  reg1=|9> reg2=|11> reg3=|4>
# 0.250000+0.000000i  reg1=|10> reg2=|12> reg3=|6>
# 0.250000+0.000000i  reg1=|11> reg2=|13> reg3=|8>
# 0.250000+0.000000i  reg1=|12> reg2=|14> reg3=|10>
# 0.250000+0.000000i  reg1=|13> reg2=|15> reg3=|12>
# 0.250000+0.000000i  reg1=|14> reg2=|0> reg3=|14>
# 0.250000+0.000000i  reg1=|15> reg2=|1> reg3=|0>

# 同样的，对结果进行了加法和溢出处理

# 最后，我们再增加一个寄存器，演示Assign（赋值）操作和Swap（交换）操作

r4 = spq.AddRegister(name='reg4', type=spq.UnsignedInteger, size=4)(state)

# 赋值操作，将r1的值赋给r4，这相当于CNOT(r1,r4) （按位）
# 注意：这里会检查两个寄存器的大小是否一致，如果不一致，则报错
spq.Assign(r1, r4)(state)
print("After Assign:")
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# SWAP操作，交换r4和r2的值
spq.Swap_General_General(r4, r2)(state)
print("After Swap:")
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# 请读者自行检查结果是否正确
# 至此，我们已经完成了量子加法的演示，更多的算术运算操作请参考pysparq的文档