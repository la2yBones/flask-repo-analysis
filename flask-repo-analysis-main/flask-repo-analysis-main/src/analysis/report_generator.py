import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import pandas as pd

class ComplexityReportGenerator:
    def __init__(self, analysis_results, output_dir):
        self.analysis_results = analysis_results
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_json_report(self):
        """生成JSON格式的详细分析报告"""
        json_path = self.output_dir / 'complexity_analysis.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, ensure_ascii=False, indent=4)
        print(f"JSON报告已生成: {json_path}")
        return json_path

    def generate_visual_report(self):
        """生成可视化图表报告"""
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文
        plt.rcParams['axes.unicode_minus'] = False

        # 1. 圈复杂度等级分布饼图
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # 圈复杂度等级分布
        cc_dist = self.analysis_results['summary']['cc_rank_distribution']
        labels = list(cc_dist.keys())
        sizes = list(cc_dist.values())
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('hls', 6))
        ax1.set_title('圈复杂度等级分布', fontsize=12)

        # 2. 文件行数TOP10
        file_level = self.analysis_results['file_level']
        file_loc = [(k, v['raw']['loc']) for k, v in file_level.items()]
        file_loc_sorted = sorted(file_loc, key=lambda x: x[1], reverse=True)[:10]
        files = [os.path.basename(f[0]) for f in file_loc_sorted]
        locs = [f[1] for f in file_loc_sorted]
        ax2.barh(files, locs, color='skyblue')
        ax2.set_xlabel('代码行数')
        ax2.set_title('文件行数TOP10', fontsize=12)
        ax2.tick_params(axis='y', labelsize=8)

        # 3. 可维护性指数分布
        mi_scores = [v['maintainability_index'] for v in file_level.values()]
        ax3.hist(mi_scores, bins=10, color='lightgreen', edgecolor='black')
        ax3.set_xlabel('可维护性指数')
        ax3.set_ylabel('文件数量')
        ax3.set_title('可维护性指数分布', fontsize=12)

        # 4. 注释率
        comment_ratio = self.analysis_results['summary']['comment_ratio']
        ax4.bar(['注释率(%)'], [comment_ratio], color='orange')
        ax4.set_ylim(0, 100)
        ax4.set_title(f'仓库整体注释率: {comment_ratio:.2f}%', fontsize=12)
        ax4.text(0, comment_ratio + 2, f'{comment_ratio:.2f}%', ha='center')

        plt.tight_layout()
        plot_path = self.output_dir / 'complexity_visualization.png'
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"可视化报告已生成: {plot_path}")
        return plot_path

    def generate_text_report(self):
        """生成文本格式的汇总报告"""
        summary = self.analysis_results['summary']
        text_content = f"""
代码库复杂度分析汇总报告
=========================
分析仓库路径: {self.output_dir.parent.parent}
分析文件总数: {summary['total_files']}
仓库总行数(LOC): {summary['total_loc']}
源代码行数(SLOC): {summary['total_sloc']}
注释行数: {summary['total_comments']}
注释率: {summary['comment_ratio']:.2f}%
总圈复杂度: {summary['total_cyclomatic_complexity']}
平均圈复杂度: {summary['avg_cyclomatic_complexity']:.2f}
平均可维护性指数: {summary['avg_maintainability_index']:.2f}

圈复杂度等级分布:
- A级(低复杂度): {summary['cc_rank_distribution']['A']}个文件
- B级: {summary['cc_rank_distribution']['B']}个文件
- C级: {summary['cc_rank_distribution']['C']}个文件
- D级: {summary['cc_rank_distribution']['D']}个文件
- E级: {summary['cc_rank_distribution']['E']}个文件
- F级(高复杂度): {summary['cc_rank_distribution']['F']}个文件

可维护性指数说明:
- 80+ : 优秀
- 60-79: 良好
- 40-59: 一般
- <40  : 差
        """
        text_path = self.output_dir / 'complexity_summary.txt'
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
        print(f"文本汇总报告已生成: {text_path}")
        return text_path

    def generate_all_reports(self):
        """生成所有类型的报告"""
        self.generate_json_report()
        self.generate_text_report()
        self.generate_visual_report()
        print(f"所有报告已生成至: {self.output_dir}")