import sys
import os

# 获取项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 将 /lib 目录添加到 PYTHONPATH
lib_path = os.path.join(project_root, 'lib')
sys.path.append(lib_path)
