import numpy as np
import pysparq as sq

from .qram import solve, classical2quantum

_classical2quantum = sq.qda_classical2quantum
_solve = sq.qda_solve
