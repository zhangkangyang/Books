"""
setup.py - 支持多种源码保护方案的打包配置
"""
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import os
import shutil

# 方案1: 使用 pyarmor 加密（需要先安装: pip install pyarmor）
# 方案2: 使用 Cython 编译（需要先安装: pip install cython）
# 方案3: 只打包 .pyc 字节码文件

class BuildPyWithProtection(build_py):
    """
    自定义构建类，可以在构建时应用保护措施
    """
    def run(self):
        # 在这里可以添加加密/混淆逻辑
        # 例如：调用 pyarmor 或 Cython
        
        # 调用父类的构建方法
        super().run()
        
        # 构建后处理：可以删除源文件，只保留 .pyc
        if os.environ.get('PROTECT_SOURCE') == 'pyc_only':
            self._remove_py_files()
    
    def _remove_py_files(self):
        """移除 .py 文件，只保留 .pyc"""
        for root, dirs, files in os.walk(self.build_lib):
            for file in files:
                if file.endswith('.py') and not file.endswith('__init__.py'):
                    py_file = os.path.join(root, file)
                    pyc_file = py_file + 'c'
                    if os.path.exists(pyc_file):
                        os.remove(py_file)
                        print(f"Removed source file: {py_file}")

setup(
    name='my-protected-module',
    version='1.0.0',
    description='演示 Python 源码保护的示例项目',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    python_requires='>=3.7',
    cmdclass={
        'build_py': BuildPyWithProtection,
    },
    install_requires=[
        # 添加你的依赖
    ],
)
