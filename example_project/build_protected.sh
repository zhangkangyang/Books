#!/bin/bash
# 综合保护方案构建脚本
# 支持多种保护方式

set -e

PROTECTION_METHOD=${1:-"pyc"}  # 默认使用 pyc 方式

echo "=== Python 源码保护构建脚本 ==="
echo "保护方式: $PROTECTION_METHOD"
echo ""

case $PROTECTION_METHOD in
    "pyc")
        echo "方案1: 只打包字节码文件 (.pyc)"
        echo "设置环境变量 PROTECT_SOURCE=pyc_only"
        PROTECT_SOURCE=pyc_only python setup.py bdist_wheel
        ;;
    
    "cython")
        echo "方案2: 使用 Cython 编译为 C 扩展"
        if ! command -v cython &> /dev/null; then
            echo "错误: 未安装 Cython"
            echo "请先安装: pip install cython"
            exit 1
        fi
        python setup_cython.py bdist_wheel
        ;;
    
    "pyarmor")
        echo "方案3: 使用 PyArmor 加密"
        bash pyarmor_build.sh
        ;;
    
    *)
        echo "未知的保护方式: $PROTECTION_METHOD"
        echo "支持的方式: pyc, cython, pyarmor"
        exit 1
        ;;
esac

echo ""
echo "=== 构建完成 ==="
