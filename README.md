这是一个为您项目量身定制的 `README.md` 文件。它采用 Markdown 格式，详细说明了项目的背景、安装步骤、使用方法以及结果分析。

---

# Flask 开源项目演化与代码特征分析工具

本项目旨在分析流行 Web 框架 **Flask** 的历史提交规律、代码演化特点以及逻辑安全性。通过结合静态分析、动态分析和形式化验证技术，揭示开源软件的演进现象。

## 🚀 核心功能

*   **演化规律提取 (Git Mining)**：自动化分析 Git 提交记录，统计功能开发与 Bug 修复的演变趋势。
*   **静态特征扫描 (AST)**：利用抽象语法树分析 Flask 路由定义、异步视图函数的使用比例。
*   **代码自动重构 (LibCST)**：模拟开源项目 API 迁移过程，实现代码树级别的精准转换。
*   **形式化安全验证 (Z3 Solver)**：将权限控制逻辑数学化，验证路由访问是否存在逻辑冲突。
*   **动态运行追踪 (PySnooper)**：实时追踪 Flask 请求处理流程中的变量变化。

---

## 📂 项目结构

```text
flask_analyzer_pro/
├── data/                  # 存储分析数据与报告
│   ├── raw/               # 存放 Flask 源码仓库 (需手动 git clone)
│   ├── processed/         # 存放清洗后的 CSV 历史数据
│   └── output/            # 存放生成的 PNG 图表与 Markdown 报告
├── src/                   # 核心源码
│   ├── data_processing/   # Git 历史提取逻辑
│   ├── analysis/          # AST、LibCST、Z3 分析模块
│   ├── utils/             # 可视化与日志工具
│   └── app.py             # 动态追踪演示 (Flask Web 入口)
├── scripts/               # 自动化脚本
│   └── run_all.py         # 一键运行全流程分析
└── requirements.txt       # 项目依赖清单
```

---

## 🛠️ 环境准备

### 1. 安装依赖
请确保您的机器已安装 Python 3.8+，执行：
```bash
pip install -r requirements.txt
```

### 2. 准备分析目标
本项目默认分析 Flask 官方仓库。请在项目根目录下执行：
```bash
mkdir -p data/raw
git clone https://github.com/pallets/flask.git data/raw/flask
```

---

## 📈 使用方法

### 1. 一键全自动分析 (推荐)
运行 `run_all.py` 脚本，它会自动提取历史、绘制图表并生成报告。

*   **默认分析 (最近 500 条提交)**：
    ```bash
    python scripts/run_all.py
    ```
*   **自定义范围分析 (分析 2022 年至今的 1000 条数据)**：
    ```bash
    python scripts/run_all.py --since 2022-01-01 --limit 1000
    ```

### 2. 动态分析与追踪
启动内置的演示 Web 服务，观察程序如何动态记录请求内部状态：
```bash
python src/app.py
```
访问 `http://127.0.0.1:5000/analyze/safety`，并在控制台中查看 **PySnooper** 输出的变量追踪日志。

---

## 📊 查看分析结果

执行完成后，您可以在以下位置找到分析成果：

1.  **直观图表**：`data/output/evolution_charts.png`
    *   *左图 (环形图)*：展示了 Feature、Bugfix、Docs 等任务的分布比例。
    *   *右图 (趋势图)*：展示了 Flask 在选定时间段内的开发活跃度波动。
2.  **详细报告**：`data/output/Analysis_Report.md`
    *   包含自动生成的 Markdown 表格、Z3 逻辑验证结论以及代码扫描摘要。
3.  **原始统计**：`data/processed/flask_history.csv`
    *   可用于 Excel 进行二次数据挖掘。

---

## 🔬 使用到的技术库
*   **ast**: Python 原生库，用于代码结构静态扫描。
*   **libcst**: 用于在保持代码格式的前提下进行语法树重构。
*   **z3-solver**: 微软开发的定理证明器，用于逻辑冲突验证。
*   **pysnooper**: 低侵入式的代码流追踪工具。
*   **GitPython**: 封装了 Git 命令，用于提取仓库元数据。

---

## 📄 许可证
本项目仅供学术研究与题目分析使用。
