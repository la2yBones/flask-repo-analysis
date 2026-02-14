# -*- coding: utf-8 -*-
import argparse
import sys
import os
import json
from datetime import datetime


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processing.git_processor import FlaskEvolutionMiner
from src.config import ANALYSIS_CONFIG, SCAN_CONFIG
from src.analysis.ast_scanner import analyze_flask_project
from src.analysis.z3_verifier import verify_route_permission
from src.analysis.cst_transformer import refactor_code_sample
from src.utils.visualizer import plot_evolution_charts
from src.utils.logger import get_logger

logger = get_logger("MainRunner")

def generate_final_report(args, ast_results, z3_results):
    """生成 Markdown 报告 """
    report_path = SCAN_CONFIG["report_md"]
    
    if "consistent" in z3_results:
        security_status = "SAFE: Logic is consistent"
        security_note = "逻辑严密，未发现潜在越权路径。"
    else:
        security_status = "WARNING: Logic Conflict Found"
        security_note = "发现逻辑冲突，需人工介入审计。"

    route_table = "| ID | Route Path | Status |\n| :--- | :--- | :--- |\n"
    for i, r in enumerate(ast_results['routes'][:10]):
        route_table += f"| {i+1} | `{r}` | Success |\n"

    markdown_content = f"""# 📊 Flask 开源项目演化分析报告

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📅 1. 分析元数据
| 项目 | 配置详情 |
| :--- | :--- |
| **本地路径** | `{args.repo}` |
| **起始日期** | `{args.since}` |
| **分析上限** | `{args.limit}` 条 |

---

## 📈 2. 演化规律可视化
![演化图表](../output/evolution_charts.png)

---

## 🔍 3. 源码静态特征 (AST)
### 路由快照
{route_table}

**统计:**
- **总路由数**: `{len(ast_results['routes'])}`
- **异步视图**: `{ast_results['async_views']}`

---

## 🛡️ 4. 安全逻辑验证 (Z3)
```lisp
{z3_results}
安全结论: {"✅ 逻辑严密" if "consistent" in z3_results else "⚠️ 发现冲突"}"""

    # 确保输出目录存在
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

# 显式指定使用 utf-8 编码写入文件
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    logger.info(f"Report generated successfully at: {report_path}")

def main():
    parser = argparse.ArgumentParser(description="Flask 一键分析工具")
    parser.add_argument("--limit", type=int, default=ANALYSIS_CONFIG["max_commits"])
    parser.add_argument("--since", type=str, default=ANALYSIS_CONFIG["since_date"])
    parser.add_argument("--until", type=str, default=ANALYSIS_CONFIG["until_date"])
    parser.add_argument("--repo", type=str, default=ANALYSIS_CONFIG["repo_path"])
    args = parser.parse_args()

    for d in ["./data/raw", "./data/processed", "./data/output"]:
        os.makedirs(d, exist_ok=True)

    if os.path.exists(args.repo):
        miner = FlaskEvolutionMiner(args.repo)
        miner.extract_commit_history(ANALYSIS_CONFIG["output_csv"], args.limit, args.since, args.until)
        plot_evolution_charts(ANALYSIS_CONFIG["output_csv"], "./data/output")
    
    ast_res = analyze_flask_project("./src")
    z3_res = verify_route_permission("User", "Admin")
    
    # 执行报告生成
    generate_final_report(args, ast_res, z3_res)
    print("\n任务完成，请查看 data/output/Analysis_Report.md")

if __name__ == "__main__":
    main()