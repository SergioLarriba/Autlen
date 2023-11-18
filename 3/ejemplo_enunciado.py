import ast
from ast import iter_fields, AST
class ASTNestedIfCounter(ast.NodeVisitor):

    def __init__(self):
        level=0
        node_name=0

    def generic_visit(self,node):
        print(f"Visiting",{type(node)})
        for field,value in ast,iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    print("\t",type(item))
                    if isinstance(item.ast.AST):
                        self.visit(item)



    


    def visit_if(self,node):
        print("Estoy en un if")



