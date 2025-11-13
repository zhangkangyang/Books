# Python whl 包源码保护完整指南

## 📋 目录

1. [保护方案概述](#保护方案概述)
2. [方案详细对比](#方案详细对比)
3. [实施步骤](#实施步骤)
4. [常见问题](#常见问题)
5. [安全建议](#安全建议)

## 保护方案概述

### 1. 字节码保护 (.pyc)

**原理**: Python 会将 .py 文件编译为字节码 .pyc，只分发字节码文件。

**实施**:
```python
# setup.py 中移除 .py 文件
import compileall
compileall.compile_dir('my_module', force=True)
# 然后删除所有 .py 文件（保留 __init__.py）
```

**保护强度**: ⭐⭐ (2/5)  
**优点**: 
- 实现简单
- 无性能影响
- 兼容性好

**缺点**:
- 可以反编译（使用 uncompyle6, decompyle3 等工具）
- 保护效果有限

### 2. PyArmor 加密

**原理**: 使用加密算法加密源码，运行时通过内置解释器解密执行。

**安装**:
```bash
pip install pyarmor
```

**使用**:
```bash
# 加密整个包
pyarmor gen --recursive --output dist_protected my_module/

# 加密并设置过期时间
pyarmor gen --expired 2024-12-31 my_module/

# 绑定到特定机器
pyarmor gen --bind-disk "100304PBN2081SF3NJ5T" my_module/
```

**保护强度**: ⭐⭐⭐ (3/5)  
**优点**:
- 使用简单
- 支持许可证控制
- 支持绑定硬件

**缺点**:
- 免费版功能有限
- 可能有性能开销
- 需要运行时解密

### 3. Cython 编译

**原理**: 将 Python 代码编译为 C 扩展模块 (.so/.pyd)，需要反汇编 C 代码才能看到逻辑。

**安装**:
```bash
pip install cython
```

**使用**:
```python
# setup_cython.py
from Cython.Build import cythonize
extensions = [
    Extension("my_module.core", ["my_module/core.py"])
]
setup(ext_modules=cythonize(extensions))
```

**保护强度**: ⭐⭐⭐⭐ (4/5)  
**优点**:
- 保护强度高
- 性能提升明显
- 难以逆向

**缺点**:
- 需要编译环境
- 可能影响兼容性
- 编译时间较长

### 4. Nuitka 编译

**原理**: 将 Python 编译为 C++ 可执行文件或扩展模块。

**安装**:
```bash
pip install nuitka
```

**使用**:
```bash
# 编译为扩展模块
python -m nuitka --module my_module/core.py
```

**保护强度**: ⭐⭐⭐⭐ (4/5)  
**优点**:
- 保护强度很高
- 性能优秀
- 可以编译为独立可执行文件

**缺点**:
- 编译时间长
- 文件体积较大
- 需要编译环境

### 5. 代码混淆

**工具**: 
- **pyobfuscate**: Python 代码混淆器
- **Opy**: 字节码混淆器
- **商业工具**: 如 VMProtect

**保护强度**: ⭐⭐⭐ (3/5)  
**优点**:
- 增加阅读难度
- 不影响性能

**缺点**:
- 可以反混淆
- 可能影响调试

## 方案详细对比

| 特性 | .pyc | PyArmor | Cython | Nuitka | 混淆 |
|------|------|---------|--------|--------|------|
| 保护强度 | 低 | 中 | 高 | 高 | 中 |
| 实施难度 | 简单 | 简单 | 中等 | 中等 | 简单 |
| 性能影响 | 无 | 轻微 | 提升 | 提升 | 无 |
| 兼容性 | 优秀 | 良好 | 良好 | 一般 | 优秀 |
| 文件大小 | 小 | 小 | 中等 | 大 | 小 |
| 编译时间 | 快 | 快 | 中等 | 慢 | 快 |
| 成本 | 免费 | 免费/付费 | 免费 | 免费/付费 | 免费/付费 |

## 实施步骤

### 方案 A: 快速方案（.pyc + 混淆）

```bash
# 1. 安装混淆工具（可选）
pip install pyobfuscate

# 2. 修改 setup.py，添加自定义构建类
# （参考 example_project/setup.py）

# 3. 构建
PROTECT_SOURCE=pyc_only python setup.py bdist_wheel
```

### 方案 B: 平衡方案（PyArmor）

```bash
# 1. 安装 PyArmor
pip install pyarmor

# 2. 加密源码
pyarmor gen --recursive --output dist_protected my_module/

# 3. 在 dist_protected 目录中构建 whl
cd dist_protected
python setup.py bdist_wheel
```

### 方案 C: 高保护方案（Cython）

```bash
# 1. 安装 Cython
pip install cython

# 2. 使用 Cython setup 文件构建
python setup_cython.py bdist_wheel

# 3. 验证生成的 .so/.pyd 文件
```

### 方案 D: 混合方案（推荐）

```python
# 1. 核心算法用 Cython 编译
# 2. 其他代码用 PyArmor 加密
# 3. 整体打包时移除源文件
```

## 常见问题

### Q1: 哪种方案最好？

**A**: 没有绝对最好的方案，建议：
- **快速上线**: 使用 .pyc + 混淆
- **平衡保护**: 使用 PyArmor
- **高保护需求**: 使用 Cython 或 Nuitka
- **最佳方案**: 混合使用（核心代码 Cython，其他 PyArmor）

### Q2: 能否完全防止逆向？

**A**: **不能**。任何保护措施都可以被破解，只是难度不同：
- .pyc → 可以反编译
- PyArmor → 可以分析运行时行为
- Cython → 可以反汇编 C 代码
- 混淆 → 可以反混淆

**建议**: 重要逻辑放在服务器端，客户端只做展示。

### Q3: 保护后如何调试？

**A**: 
- 保留未保护的开发版本
- 使用条件编译：`if DEBUG: 使用源码 else: 使用保护版本`
- 使用日志系统辅助调试

### Q4: 会影响性能吗？

**A**: 
- .pyc: 无影响（Python 本身就会生成）
- PyArmor: 轻微影响（运行时解密）
- Cython: 通常提升性能
- Nuitka: 通常提升性能

### Q5: 如何测试保护后的包？

**A**: 
```bash
# 1. 构建保护后的 whl
python setup.py bdist_wheel

# 2. 安装到测试环境
pip install dist/my_module-1.0.0-py3-none-any.whl --force-reinstall

# 3. 运行测试
python test_module.py
```

## 安全建议

### 1. 多层防护

不要依赖单一保护措施：
```
源码 → 混淆 → Cython编译 → PyArmor加密 → 打包
```

### 2. 关键代码分离

- **客户端**: 只包含展示逻辑
- **服务器端**: 核心算法和业务逻辑
- **API 调用**: 使用加密通信

### 3. 许可证控制

使用 PyArmor 的许可证功能：
```bash
pyarmor licenses --expired 2024-12-31 r001
pyarmor gen --with-license licenses/r001/license.lic my_module/
```

### 4. 定期更新

- 定期更新保护工具版本
- 更换加密算法和密钥
- 监控破解情况

### 5. 法律保护

- 使用软件许可协议
- 明确禁止逆向工程
- 必要时采取法律手段

## 实际案例

### 案例 1: 游戏客户端保护

```python
# 使用 Cython 编译核心算法
# 使用 PyArmor 保护配置和资源路径
# 服务器端验证关键操作
```

### 案例 2: 商业软件保护

```python
# 使用 Nuitka 编译为可执行文件
# 集成硬件绑定
# 在线许可证验证
```

### 案例 3: 开源软件商业化

```python
# 核心功能开源
# 高级功能使用 Cython 编译
# 通过许可证控制访问
```

## 总结

1. **没有完美的保护方案** - 只能增加破解难度
2. **选择合适的方案** - 根据需求平衡保护强度和成本
3. **多层防护** - 结合多种方案使用
4. **服务器端验证** - 重要逻辑不要放在客户端
5. **持续更新** - 定期更新保护措施

记住：**最好的保护是将关键逻辑放在服务器端，客户端只做展示和交互。**
