# PySparq 量子计算教程 - 寄存器全局管理

## 寄存器命名空间机制

### 核心特性
- **全局命名空间**：所有量子态共享寄存器元数据
- **状态独立性**：量子态数据互相独立，但寄存器定义全局共享
- **限制表现**：
  ```python
  # 不同量子态实例无法维护独立寄存器配置
  state1 = spq.SparseState()
  state2 = spq.SparseState()  # 强制共享寄存器定义
  ```

## 系统重置方法

### 方案对比
| 方法 | 操作方式 | 适用场景 | 注意事项 |
|------|----------|----------|----------|
| **寄存器删除** | `RemoveRegister` 逐条移除 | 局部调整寄存器配置 | 需精确控制寄存器生命周期 |
| **系统清空** | `spq.System.clear()` 全局重置 | 完全重新初始化系统 | 影响所有现存量子态实例 |

## 操作演示

### 初始系统状态
```python
state = spq.SparseState()
r1 = spq.AddRegister(name='reg1', type=spq.UnsignedInteger, size=4)(state)
r2 = spq.AddRegister(name='reg2', type=spq.UnsignedInteger, size=3)(state)

spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)
```
输出特征：
```text
|(0)reg1 : UInt4 | |(1)reg2 : UInt3 | 
1.000000+0.000000i  reg1=|0> reg2=|0>
```

### 执行系统清空
```python
spq.System.clear()  # 全局寄存器配置重置
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)
```
输出变化：
```text
1.000000+0.000000i  # 寄存器元数据完全消失
```

### 重建寄存器配置
```python
r3 = spq.AddRegister(name='reg3', type=spq.UnsignedInteger, size=4)(state)
spq.StatePrint(disp=spq.StatePrintDisplay.Detail)(state)
```
新配置输出：
```text
|(0)reg3 : UInt4 | 
1.000000+0.000000i  reg3=|0>
```

## 关键注意事项

### 系统清空影响
⚠️ **重要警告**：
- 清空操作会将所有内部状态全部恢复到程序初始化状态
- 现存量子态(`SparseState`)实例的含义基本失效，必须重新申请
- 后续操作必须重新申请寄存器

### 寄存器删除方法
```python
# 示例删除操作（需记录寄存器ID）
spq.RemoveRegister(register_id=0)(state)
```

## 最佳实践建议

1. **实验流程管理**：
   ```python
   def reset_system():
       spq.System.clear()
       return spq.SparseState()  # 返回新量子态实例
   ```

2. **配置保存方案**：
   ```python
   # 保存寄存器配置模板
   config_template = [
       {'name':'main', 'type':spq.UnsignedInteger, 'size':8},
       {'name':'ctrl', 'type':spq.General, 'size':2}
   ]
   
   def rebuild_system(config):
       spq.System.clear()
       state = spq.SparseState()
       for params in config:
           spq.AddRegister(**params)(state)
       return state
   ```
