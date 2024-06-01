import ast
from export_ast import ast_to_dict
import json

code = """
print('Hello World!')

CodebaseExtractor().run()
"""
tree = ast.parse(code)

d = ast_to_dict(tree)

# Or as AST string (indent must be >0)...
tree_str = ast.dump(tree, indent=2)
d = ast_to_dict(tree_str)

def save_as_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

save_as_json(d, 'ast.json')