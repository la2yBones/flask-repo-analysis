import pysnooper
import tempfile
from flask import Flask, jsonify, request, send_file
from src.analysis.z3_verifier import verify_route_permission
from pathlib import Path
from src.analysis.complexity_analyzer import CodeComplexityAnalyzer
from src.analysis.report_generator import ComplexityReportGenerator
from src.data_processing.complexity_processor import save_complexity_data_to_csv


app = Flask(__name__)

@app.route('/analyze/safety')
@pysnooper.snoop() # 动态追踪此接口的执行过程
def safety_check():
    # 模拟对应用逻辑的实时形式化验证
    result = verify_route_permission("user", "admin")
    return jsonify({"z3_report": result})

APP_OUTPUT_DIR = Path('./data')

@app.route('/api/analyze-complexity', methods=['POST'])
def analyze_complexity():
    """
    接口：触发代码库复杂度分析
    请求参数：{"repo_path": "代码仓库路径"}
    返回：分析结果汇总 + 报告路径
    """
    try:
        data = request.get_json()
        repo_path = data.get('repo_path')
        if not repo_path or not Path(repo_path).exists():
            return jsonify({'code': 400, 'msg': '无效的仓库路径'}), 400

        # 执行分析
        analyzer = CodeComplexityAnalyzer(repo_path)
        analysis_results = analyzer.analyze_repo()

        # 保存数据并生成报告
        temp_dir = tempfile.mkdtemp(dir=str(APP_OUTPUT_DIR / 'output'))
        report_generator = ComplexityReportGenerator(analysis_results, temp_dir)
        report_generator.generate_all_reports()
        save_complexity_data_to_csv(analysis_results, APP_OUTPUT_DIR / 'processed' / 'complexity_data')

        return jsonify({
            'code': 200,
            'msg': '分析成功',
            'summary': analysis_results['summary'],
            'report_dir': temp_dir,
            'tips': '可通过/api/get-report接口获取报告文件'
        }), 200

    except Exception as e:
        return jsonify({'code': 500, 'msg': f'分析失败: {str(e)}'}), 500

@app.route('/api/get-report/<report_type>', methods=['GET'])
def get_report(report_type):
    """
    接口：获取分析报告文件
    report_type: json/text/visual/csv
    """
    try:
        report_dir = request.args.get('report_dir')
        if not report_dir or not Path(report_dir).exists():
            return jsonify({'code': 400, 'msg': '无效的报告目录'}), 400

        report_paths = {
            'json': Path(report_dir) / 'complexity_analysis.json',
            'text': Path(report_dir) / 'complexity_summary.txt',
            'visual': Path(report_dir) / 'complexity_visualization.png',
            'csv': APP_OUTPUT_DIR / 'processed' / 'complexity_data' / 'complexity_file_level.csv'
        }

        target_file = report_paths.get(report_type)
        if not target_file or not target_file.exists():
            return jsonify({'code': 404, 'msg': '报告文件不存在'}), 404

        return send_file(str(target_file), as_attachment=True)

    except Exception as e:
        return jsonify({'code': 500, 'msg': f'获取报告失败: {str(e)}'}), 500

@app.route('/')
def index():
    return """
    <h1>代码库复杂度分析工具</h1>
    <p>使用接口：</p>
    <ul>
        <li>POST /api/analyze-complexity - 触发分析，参数{"repo_path": "仓库路径"}</li>
        <li>GET /api/get-report/[json/text/visual/csv]?report_dir=报告目录 - 获取报告文件</li>
    </ul>
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)