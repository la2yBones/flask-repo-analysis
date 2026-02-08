import argparse
from pathlib import Path
from src.analysis.complexity_analyzer import CodeComplexityAnalyzer
from src.analysis.report_generator import ComplexityReportGenerator
from src.data_processing.complexity_processor import save_complexity_data_to_csv

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='代码库复杂度分析工具')
    parser.add_argument('--repo-path', required=True, help='要分析的代码仓库路径')
    parser.add_argument('--output-dir', default='./data', help='分析结果输出目录')
    args = parser.parse_args()

    # 验证仓库路径
    repo_path = Path(args.repo_path)
    if not repo_path.exists():
        print(f"错误: 仓库路径{repo_path}不存在")
        return

    # 1. 执行复杂度分析
    print(f"开始分析仓库: {repo_path}")
    analyzer = CodeComplexityAnalyzer(str(repo_path))
    analysis_results = analyzer.analyze_repo()
    print("复杂度分析完成")

    # 2. 保存处理后的数据
    processed_dir = Path(args.output_dir) / 'processed' / 'complexity_data'
    save_complexity_data_to_csv(analysis_results, processed_dir)

    # 3. 生成报告
    report_dir = Path(args.output_dir) / 'output' / 'complexity_report'
    report_generator = ComplexityReportGenerator(analysis_results, report_dir)
    report_generator.generate_all_reports()

    print("所有分析流程完成！")

if __name__ == '__main__':
    main()