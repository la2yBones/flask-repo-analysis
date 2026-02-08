import pandas as pd
from pathlib import Path

def save_complexity_data_to_csv(analysis_results, output_dir):
    """
    将分析结果保存为CSV格式，便于后续分析
    :param analysis_results: 复杂度分析结果
    :param output_dir: 输出目录
    :return: CSV文件路径
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 提取文件级数据
    file_data = []
    for file_path, res in analysis_results['file_level'].items():
        row = {
            'file_path': file_path,
            'loc': res['raw']['loc'],
            'sloc': res['raw']['sloc'],
            'comments': res['raw']['comments'],
            'blank': res['raw']['blank'],
            'comment_ratio': (res['raw']['comments'] / res['raw']['loc']) * 100 if res['raw']['loc'] > 0 else 0,
            'cyclomatic_complexity_total': res['cyclomatic_complexity']['total'],
            'cyclomatic_complexity_rank': res['cyclomatic_complexity']['avg_rank'],
            'maintainability_index': res['maintainability_index'],
            'halstead_difficulty': res['halstead']['difficulty'],
            'halstead_effort': res['halstead']['effort']
        }
        file_data.append(row)
    
    # 保存为CSV
    csv_path = output_dir / 'complexity_file_level.csv'
    df = pd.DataFrame(file_data)
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    
    # 保存汇总数据
    summary_df = pd.DataFrame([analysis_results['summary']])
    summary_csv_path = output_dir / 'complexity_summary.csv'
    summary_df.to_csv(summary_csv_path, index=False, encoding='utf-8-sig')
    
    print(f"CSV数据已保存至: {csv_path} 和 {summary_csv_path}")
    return csv_path, summary_csv_path