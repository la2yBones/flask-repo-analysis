import argparse
import sys
import os

# 确保能找到 src 模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processing.git_processor import FlaskEvolutionMiner
from src.config import ANALYSIS_CONFIG
from src.analysis.ast_scanner import analyze_flask_project
from src.utils.visualizer import plot_evolution_charts

def main():
    parser = argparse.ArgumentParser(description="Flask 开源软件演化分析工具")
    
    # 添加命令行参数
    parser.add_argument("--limit", type=int, default=ANALYSIS_CONFIG["max_commits"], help="分析的提交数量限制")
    parser.add_argument("--since", type=str, default=ANALYSIS_CONFIG["since_date"], help="起始日期 (YYYY-MM-DD)")
    parser.add_argument("--until", type=str, default=ANALYSIS_CONFIG["until_date"], help="截止日期 (YYYY-MM-DD)")
    parser.add_argument("--repo", type=str, default=ANALYSIS_CONFIG["repo_path"], help="Flask 源码本地路径")
    
    args = parser.parse_args()

    # 1. 执行演化扫描
    if os.path.exists(args.repo):
        miner = FlaskEvolutionMiner(args.repo)
        miner.extract_commit_history(
            output_csv=ANALYSIS_CONFIG["output_csv"],
            limit=args.limit,
            since=args.since,
            until=args.until
        )
        # 自动生成图表
        plot_evolution_charts(ANALYSIS_CONFIG["output_csv"], "./data/output")
    else:
        print(f"错误: 找不到仓库路径 {args.repo}，请检查配置或运行 git clone")

    # 2. 执行静态分析
    print("\n执行静态 AST 特征扫描...")
    ast_res = analyze_flask_project("./src")
    print(f"路由特征提取完成: 发现 {len(ast_res['routes'])} 个路由")

if __name__ == "__main__":
    main()
    