import ast
from ast import iter_fields, AST
class ASTNestedIfCounter(ast.NodeVisitor):

    def generic_visit(self,node):
        for field, value in iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        self.visit(item)
            elif isinstance(value, AST):
                self.visit(value)

    def visit_if(self,node):
        print("Estoy en un if")