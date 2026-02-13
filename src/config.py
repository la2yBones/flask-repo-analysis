from datetime import datetime

# 分析配置
ANALYSIS_CONFIG = {
    "repo_path": "./data/raw/flask",
    "output_csv": "./data/processed/flask_history.csv",
    "max_commits": 500,           # 默认分析最近500条
    "since_date": "2020-01-01",   # 默认起始时间
    "until_date": datetime.now().strftime("%Y-%m-%d"), # 默认当前日期
}

# 静态扫描配置
SCAN_CONFIG = {
    "target_dir": "./src",
    "report_md": "./data/output/Analysis_Report.md"
}