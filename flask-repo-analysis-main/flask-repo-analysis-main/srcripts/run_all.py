import sys
import os
import json

# 确保能找到 src 模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processing.git_processor import FlaskEvolutionMiner
from src.analysis.ast_scanner import analyze_flask_project
from src.analysis.cst_transformer import refactor_code_sample
from src.analysis.z3_verifier import verify_route_permission

def main():
    print("--- 1. Git 演化规律分析 ---")
    repo_path = "./data/raw/flask"
    if os.path.exists(repo_path):
        miner = FlaskEvolutionMiner(repo_path)
        # 增加参数限制，先跑通流程
        miner.extract_commit_history("./data/processed/flask_history.csv", max_commits=200)
    else:
        print("请在 data/raw/flask 下放入 Flask 源码仓库以进行完整分析。")

    print("\n--- 2. AST 静态扫描示例 ---")
    fake_code_dir = "./src" # 扫描本项目源码作为示例
    stats = analyze_flask_project(fake_code_dir)
    print(f"扫描结果: {json.dumps(stats, indent=2)}")

    print("\n--- 3. LibCST 代码重构演化 ---")
    old_code = "from flask import Flask, Markup\nm = Markup('<b>Hi</b>')"
    new_code = refactor_code_sample(old_code)
    print(f"旧代码:\n{old_code}\n重构后:\n{new_code}")

    print("\n--- 4. Z3 逻辑安全性验证 ---")
    verify_res = verify_route_permission("any", "admin")
    print(f"验证结果: {verify_res}")

if __name__ == "__main__":
    # 创建必要目录
    os.makedirs("./data/raw", exist_ok=True)
    os.makedirs("./data/processed", exist_ok=True)
    os.makedirs("./data/output", exist_ok=True)
    main()