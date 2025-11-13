"""
setup_cython.py - 使用 Cython 编译为 C 扩展的配置
需要先安装: pip install cython
"""
from setuptools import setup, Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy  # 如果不需要可以删除

# 定义需要编译的模块
extensions = [
    Extension(
        "my_module.core",
        ["my_module/core.py"],
        # 可以添加额外的编译选项
        extra_compile_args=['-O3'],  # 优化级别
    ),
]

setup(
    name='my-protected-module-cython',
    version='1.0.0',
    description='使用 Cython 保护的 Python 模块',
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",  # Python 3
            'boundscheck': False,   # 禁用边界检查以提高性能
            'wraparound': False,    # 禁用负索引包装
        },
        build_dir="build"
    ),
    cmdclass={'build_ext': build_ext},
    zip_safe=False,
)
