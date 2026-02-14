import sys
import os

# 获取项目根目录（E:\Code\hw\flask）
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将根目录加入Python路径
sys.path.append(ROOT_DIR)

import pysnooper
from flask import Flask, jsonify
from src.analysis.z3_verifier import verify_route_permission

app = Flask(__name__)

@app.route('/analyze/safety')
@pysnooper.snoop() # 动态追踪此接口的执行过程
def safety_check():
    # 模拟对应用逻辑的实时形式化验证
    result = verify_route_permission("user", "admin")
    return jsonify({"z3_report": result})

if __name__ == "__main__":
    app.run(debug=True)