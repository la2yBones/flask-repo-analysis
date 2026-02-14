import ast
import os

class FlaskFeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.results = {
            "routes": [], 
            "async_views": 0,
            "func_lengths": [],
            "decorators": {}
        }

    def visit_FunctionDef(self, node):
        # 记录函数行数用于复杂度分析
        length = node.end_lineno - node.lineno
        self.results["func_lengths"].append(length)

        # 1. 识别装饰器路由 (如 @app.route, @blueprint.route, @route)
        for deco in node.decorator_list:
            deco_name = ""
            # 处理 @app.route('/') 这种 Call 形式
            if isinstance(deco, ast.Call):
                func = deco.func
                # 处理 app.route
                if isinstance(func, ast.Attribute):
                    deco_name = func.attr
                # 处理 route
                elif isinstance(func, ast.Name):
                    deco_name = func.id
                
                if deco_name == 'route':
                    # 提取路由路径
                    if deco.args and isinstance(deco.args[0], ast.Constant):
                        self.results["routes"].append(str(deco.args[0].value))
                    else:
                        self.results["routes"].append("dynamic_route")

            # 记录装饰器频率
            if deco_name:
                self.results["decorators"][deco_name] = self.results["decorators"].get(deco_name, 0) + 1

        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        # 增加对异步函数的统计
        self.results["async_views"] += 1
        self.visit_FunctionDef(node) # 异步函数也可能是路由

    def visit_Call(self, node):
        # 2. 识别非装饰器路由 (如 app.add_url_rule('/', ...))
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'add_url_rule':
            if node.args and isinstance(node.args[0], ast.Constant):
                self.results["routes"].append(str(node.args[0].value))
        self.generic_visit(node)

def analyze_flask_project(target_path):
    visitor = FlaskFeatureVisitor()
    if not os.path.exists(target_path):
        return visitor.results

    for root, _, files in os.walk(target_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                        visitor.visit(tree)
                except Exception:
                    continue
    return visitor.results