import sys
import os
import argparse
from datetime import datetime

# 确保能找到 src 模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.visualizer import plot_evolution_charts
from src.analysis.ast_scanner import analyze_flask_project
from src.analysis.z3_verifier import verify_route_permission
from src.config import ANALYSIS_CONFIG

def generate_markdown_report(args):
    """生成 Markdown 报告，接收 args 参数以获取时间范围"""
    print(f"正在生成分析报告 (范围: {args.since} 至 {args.until})...")
    
    # 1. 执行可视化 (确保数据文件存在)
    csv_path = ANALYSIS_CONFIG["output_csv"]
    plot_evolution_charts(csv_path, "./data/output")

    # 2. 收集分析数据
    ast_results = analyze_flask_project("./src") 
    z3_results = verify_route_permission("User", "Admin")

    # 3. 编写 Markdown 内容
    report_content = f"""
# Flask 开源软件演化与安全性分析报告

## 0. 分析元数据
- **报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **分析数量限制**: {args.limit} 条提交
- **时间范围**: {args.since} 至 {args.until}

## 1. 仓库演化规律分析
![演化图表](../output/evolution_charts.png)
*注：饼图展示了指定时间范围内 Flask 维护类型的分布。*

## 2. 代码特点静态扫描 (AST)
基于抽象语法树分析，当前代码库特征如下：
- **检测到的路由数量**: {len(ast_results['routes'])}
- **异步视图函数 (Async Views)**: {ast_results['async_views']}

## 3. 安全逻辑形式化验证 (Z3 Solver)
- **验证结论**: `{z3_results}`

---
*报告由 Flask Evolution Analyzer 自动生成*
"""

    report_path = "./data/output/Analysis_Report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"Markdown 报告已成功生成: {report_path}")

if __name__ == "__main__":
    # 1. 同样配置参数解析器，确保与 run_all.py 一致
    parser = argparse.ArgumentParser(description="生成分析报告")
    parser.add_argument("--limit", type=int, default=ANALYSIS_CONFIG["max_commits"])
    parser.add_argument("--since", type=str, default=ANALYSIS_CONFIG["since_date"])
    parser.add_argument("--until", type=str, default=ANALYSIS_CONFIG["until_date"])
    
    args = parser.parse_args()

    # 2. 传入 args 调用函数
    generate_markdown_report(args)