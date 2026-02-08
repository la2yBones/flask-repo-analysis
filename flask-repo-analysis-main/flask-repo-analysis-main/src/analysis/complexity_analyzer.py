import radon
from radon.complexity import cc_visit, cc_rank
from radon.metrics import h_visit, mi_visit
from radon.raw import analyze
from src.utils.file_utils import get_all_code_files, read_file_content

class CodeComplexityAnalyzer:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.code_files = get_all_code_files(repo_path)
        self.analysis_results = {
            'file_level': {},  # 按文件维度的分析结果
            'summary': {}      # 仓库级汇总结果
        }

    def analyze_single_file(self, file_path):
        """
        分析单个文件的复杂度指标
        :param file_path: 文件路径
        :return: 单个文件的分析结果字典
        """
        content = read_file_content(file_path)
        if not content:
            return None
        
        # 1. 原始指标（行数、空行、注释行等）
        raw_analysis = analyze(content)
        # 2. 圈复杂度（Cyclomatic Complexity）
        cc_analysis = cc_visit(content)
        # 3. 可维护性指数（Maintainability Index）
        mi_score = mi_visit(content, multi=True)
        # 4. Halstead指标（代码量、难度、工作量等）
        h_analysis = h_visit(content)

        # 计算该文件的圈复杂度汇总
        cc_total = sum(cc.complexity for cc in cc_analysis)
        cc_ranks = [cc_rank(cc.complexity) for cc in cc_analysis]
        cc_rank_avg = max(cc_ranks) if cc_ranks else 'A'

        return {
            'file_path': file_path,
            'raw': {
                'loc': raw_analysis.loc,          # 代码总行数
                'lloc': raw_analysis.lloc,        # 逻辑行数
                'sloc': raw_analysis.sloc,        # 源代码行数（非空非注释）
                'comments': raw_analysis.comments,# 注释行数
                'blank': raw_analysis.blank,      # 空行数
                'single_comments': raw_analysis.single_comments # 单行注释
            },
            'cyclomatic_complexity': {
                'total': cc_total,
                'avg_rank': cc_rank_avg,
                'details': [{'name': cc.name, 'complexity': cc.complexity, 'rank': cc_rank(cc.complexity)} for cc in cc_analysis]
            },
            'maintainability_index': mi_score,
            'halstead': {
                'total_operators': h_analysis.total_operators,
                'total_operands': h_analysis.total_operands,
                'vocabulary': h_analysis.vocabulary,
                'length': h_analysis.length,
                'difficulty': h_analysis.difficulty,
                'effort': h_analysis.effort,
                'time': h_analysis.time,
                'bugs': h_analysis.bugs
            }
        }

    def analyze_repo(self):
        """
        分析整个仓库的代码复杂度
        :return: 仓库级分析结果
        """
        total_files = len(self.code_files)
        if total_files == 0:
            raise ValueError(f"在仓库{self.repo_path}中未找到可分析的代码文件")

        # 遍历所有文件分析
        for file_path in self.code_files:
            file_result = self.analyze_single_file(file_path)
            if file_result:
                self.analysis_results['file_level'][file_path] = file_result

        # 计算仓库级汇总指标
        self._calculate_summary()
        return self.analysis_results

    def _calculate_summary(self):
        """
        计算仓库级的汇总复杂度指标
        """
        file_results = list(self.analysis_results['file_level'].values())
        total_loc = sum(res['raw']['loc'] for res in file_results)
        total_sloc = sum(res['raw']['sloc'] for res in file_results)
        total_comments = sum(res['raw']['comments'] for res in file_results)
        total_cc = sum(res['cyclomatic_complexity']['total'] for res in file_results)
        avg_mi = sum(res['maintainability_index'] for res in file_results) / len(file_results)

        # 统计圈复杂度等级分布
        cc_rank_dist = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0}
        for res in file_results:
            rank = res['cyclomatic_complexity']['avg_rank']
            if rank in cc_rank_dist:
                cc_rank_dist[rank] += 1

        self.analysis_results['summary'] = {
            'total_files': len(file_results),
            'total_loc': total_loc,
            'total_sloc': total_sloc,
            'total_comments': total_comments,
            'comment_ratio': (total_comments / total_loc) * 100 if total_loc > 0 else 0,
            'total_cyclomatic_complexity': total_cc,
            'avg_cyclomatic_complexity': total_cc / len(file_results) if len(file_results) > 0 else 0,
            'avg_maintainability_index': avg_mi,
            'cc_rank_distribution': cc_rank_dist
        }