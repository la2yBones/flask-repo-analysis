import libcst as cst

class FlaskLegacyFixer(cst.CSTTransformer):
    def leave_ImportFrom(self, original_node, updated_node):
        if updated_node.module.value == 'flask':
            new_names = [n for n in updated_node.names if n.name.value != 'Markup']
            if not new_names:
                return cst.RemoveFromParent()
            return updated_node.with_changes(names=new_names)
        return updated_node

def refactor_code_sample(code):
    tree = cst.parse_module(code)
    modified_tree = tree.visit(FlaskLegacyFixer())
    return modified_tree.code