import os
from pathlib import Path

def get_all_code_files(repo_path, extensions=None):
    """
    遍历仓库目录，获取所有指定后缀的代码文件
    :param repo_path: 仓库根路径
    :param extensions: 目标文件后缀列表，默认['.py']
    :return: 代码文件路径列表
    """
    if extensions is None:
        extensions = ['.py']
    
    repo_path = Path(repo_path).resolve()
    code_files = []
    
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in extensions:
                # 排除虚拟环境、__pycache__、.git等目录
                exclude_dirs = ['__pycache__', '.git', 'venv', 'env', '.env']
                if not any(ex_dir in str(file_path) for ex_dir in exclude_dirs):
                    code_files.append(str(file_path))
    
    return code_files

def read_file_content(file_path):
    """
    读取文件内容，处理编码问题
    :param file_path: 文件路径
    :return: 文件内容字符串
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                return f.read()
        except Exception as e:
            print(f"读取文件{file_path}失败: {e}")
            return ""