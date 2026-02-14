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
        # 统计函数行数
        length = node.end_lineno - node.lineno
        self.results["func_lengths"].append(length)

        # 统计装饰器
        for deco in node.decorator_list:
            name = ""
            if isinstance(deco, ast.Call):
                if isinstance(deco.func, ast.Attribute): name = deco.func.attr
                elif isinstance(deco.func, ast.Name): name = deco.func.id
            elif isinstance(deco, ast.Name): name = deco.id
            
            if name:
                self.results["decorators"][name] = self.results["decorators"].get(name, 0) + 1
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