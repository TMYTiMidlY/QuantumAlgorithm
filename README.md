# QuantumAlgorithm
A package for implementing quantum algorithms using the pysparq package.

# Installation
To install the package, run the following command in the terminal:

    pip install qalgo

# Usage
To use the package, simply import the module and create an instance of the desired algorithm class. For example:

```python
from qalgo import qda
import numpy as np

a = np.array([[1, 2], [3, 5]])
b = np.array([1, 2])
x_hat = qda.solve(a, b)
```

# Algorithms
The package currently includes the following quantum algorithms:

- Discrete adiabatic quantum linear system solver 
- Grover's algorithm (TODO)
- Hamiltonian simulation (TODO)
- Shor's algorithm (TODO)

# Documentation
The documentation for the package can be found at https://qalgo.readthedocs.io/zh-cn/latest/.