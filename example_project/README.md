# Python 源码保护方案示例

本项目演示了在打包 Python whl 包时保护源码的几种常见方案。

## ⚠️ 重要说明

**完全防止逆向破解是不可能的**，但可以通过以下方案增加破解难度：

1. **源码混淆** - 使代码难以阅读，但可以反混淆
2. **字节码保护** - 只分发 .pyc 文件，但可以反编译
3. **Cython 编译** - 编译为 C 扩展，需要反汇编 C 代码
4. **运行时加密** - 使用 PyArmor 等工具，运行时解密

## 方案对比

| 方案 | 保护强度 | 性能影响 | 兼容性 | 推荐度 |
|------|---------|---------|--------|--------|
| 只打包 .pyc | ⭐⭐ | 无 | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| PyArmor 加密 | ⭐⭐⭐ | 轻微 | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Cython 编译 | ⭐⭐⭐⭐ | 提升 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 商业混淆工具 | ⭐⭐⭐⭐ | 轻微 | ⭐⭐⭐ | ⭐⭐⭐ |

## 使用方法

### 方案1: 只打包字节码文件

```bash
# 设置环境变量后构建
PROTECT_SOURCE=pyc_only python setup.py bdist_wheel

# 或使用脚本
bash build_protected.sh pyc
```

**优点**: 简单，无需额外工具  
**缺点**: .pyc 可以反编译回 .py

### 方案2: 使用 Cython 编译

```bash
# 先安装 Cython
pip install cython

# 构建
python setup_cython.py bdist_wheel

# 或使用脚本
bash build_protected.sh cython
```

**优点**: 保护强度较高，性能提升  
**缺点**: 需要编译环境，可能影响兼容性

### 方案3: 使用 PyArmor 加密

```bash
# 先安装 PyArmor
pip install pyarmor

# 使用脚本构建
bash pyarmor_build.sh

# 或使用脚本
bash build_protected.sh pyarmor
```

**优点**: 使用简单，保护效果较好  
**缺点**: 需要运行时解密，可能有性能开销

## 其他工具推荐

### 1. PyArmor (推荐)
- 官网: https://pyarmor.readthedocs.io/
- 功能: 源码加密、混淆、许可证控制
- 免费版功能有限，商业版功能更强

### 2. Nuitka
- 官网: https://nuitka.net/
- 功能: 将 Python 编译为 C++ 可执行文件
- 可以编译为扩展模块

### 3. Opy
- GitHub: https://github.com/QQuick/Opy
- 功能: Python 字节码混淆器

### 4. 商业工具
- **VMProtect** - 虚拟机保护
- **Themida** - 代码保护
- **Enigma Protector** - 打包和保护

## 最佳实践

1. **多层防护**: 结合多种方案使用
2. **关键代码用 Cython**: 核心算法用 Cython 编译
3. **服务器端验证**: 重要逻辑放在服务器端
4. **许可证控制**: 使用 PyArmor 的许可证功能
5. **代码混淆**: 使用混淆工具增加阅读难度

## 注意事项

1. **法律合规**: 确保你的保护措施符合相关法律法规
2. **兼容性测试**: 在不同平台和 Python 版本上测试
3. **性能影响**: 评估保护措施对性能的影响
4. **维护成本**: 考虑后续维护和更新的成本

## 示例代码

```python
# 使用示例
from my_module import calculate_secret, process_data

# 调用被保护的函数
result = calculate_secret(123)
print(f"结果: {result}")

data = [1, 2, 3, 4, 5]
processed = process_data(data)
print(f"处理结果: {processed}")
```

## 参考资料

- [PyArmor 文档](https://pyarmor.readthedocs.io/)
- [Cython 文档](https://cython.readthedocs.io/)
- [Python 打包指南](https://packaging.python.org/)
