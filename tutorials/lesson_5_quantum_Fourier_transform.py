'''这里我们演示pysparq中的quantum Fourier transform
'''


import pysparq as spq

state = spq.SparseState()

r1 = spq.AddRegister(name='reg1', type=spq.UnsignedInteger, size=4)(state)

# 对r1执行QFT
spq.QFT(r1)(state)


# 打印量子态
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# StatePrint (mode=Detail)
# |(0)reg1 : UInt4 | 
# 0.250000+0.000000i  reg1=|0>
# 0.250000+0.000000i  reg1=|1>
# 0.250000+0.000000i  reg1=|2>
# 0.250000+0.000000i  reg1=|3>
# 0.250000+0.000000i  reg1=|4>
# 0.250000+0.000000i  reg1=|5>
# 0.250000+0.000000i  reg1=|6>
# 0.250000+0.000000i  reg1=|7>
# 0.250000+0.000000i  reg1=|8>
# 0.250000+0.000000i  reg1=|9>
# 0.250000+0.000000i  reg1=|10>
# 0.250000+0.000000i  reg1=|11>
# 0.250000+0.000000i  reg1=|12>
# 0.250000+0.000000i  reg1=|13>
# 0.250000+0.000000i  reg1=|14>
# 0.250000+0.000000i  reg1=|15>

# 这里对reg1的最低位执行Z门，改变相位
spq.Zgate_Bool(r1, 0)(state)

print("After Z:")
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# 然后再执行QFT
spq.QFT(r1)(state)

print("After QFT:")
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)

# 输出：
# After QFT:
# StatePrint (mode=Detail)
# |(0)reg1 : UInt4 |
# 1.000000+0.000000i  reg1=|8>
# 读者可以自行用理论检查结果是否正确
