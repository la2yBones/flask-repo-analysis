import ast
import os

class FlaskFeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.results = {"routes": [], "async_views": 0}

    def visit_FunctionDef(self, node):
        # 检查是否为 Flask 路由
        for deco in node.decorator_list:
            if isinstance(deco, ast.Call) and getattr(deco.func, 'attr', '') == 'route':
                route_path = deco.args[0].value if deco.args and isinstance(deco.args[0], ast.Constant) else "dynamic"
                self.results["routes"].append(route_path)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.results["async_views"] += 1
        self.generic_visit(node)

def analyze_flask_project(src_dir):
    visitor = FlaskFeatureVisitor()
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read())
                        visitor.visit(tree)
                    except: pass
    return visitor.results