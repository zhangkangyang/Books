#!/bin/bash
# pyarmor 加密构建脚本
# 使用方法: bash pyarmor_build.sh

set -e

echo "=== 使用 PyArmor 加密源码 ==="

# 检查是否安装了 pyarmor
if ! command -v pyarmor &> /dev/null; then
    echo "错误: 未安装 pyarmor"
    echo "请先安装: pip install pyarmor"
    exit 1
fi

# 清理之前的构建
echo "清理旧的构建文件..."
rm -rf build/ dist/ *.egg-info
rm -rf my_module/*.pyc my_module/__pycache__

# 使用 pyarmor 加密源码
echo "加密源码..."
pyarmor gen --recursive --output dist_protected my_module/

# 复制 setup.py 和其他必要文件
cp setup.py dist_protected/
cp README.md dist_protected/ 2>/dev/null || true

# 进入加密后的目录构建 whl
cd dist_protected
python setup.py bdist_wheel

echo ""
echo "=== 构建完成 ==="
echo "whl 文件位置: dist_protected/dist/"
