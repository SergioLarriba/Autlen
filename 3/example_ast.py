import ast
import inspect
from ast_utils import ASTNestedIfCounter
def fun1(p):
    a=1
    b=2
    if a==1:
        print(a)
    if b==1:
        print(b)
def fun2(p):
    a=1
    if a==1:
        print(a)
    if True:
        if True:
            if a==1:
                print(a)
def main() -> None:
    counter = ASTNestedIfCounter()
    source = inspect.getsource(fun1)
    my_ast = ast.parse(source)
    print("fun1: maximum number of nested if:", counter.visit(my_ast))
    # Should print 1
    source = inspect.getsource(fun2)
    my_ast = ast.parse(source)
    print("fun2: maximum number of nested if:", counter.visit(my_ast))
    # Should print 3


main()

class ASTDotVisitor(ast.NodeVisitor):
    def print_if_pos(num):
        if num > 0:
            print(num)


        source=inspect.getsource(print_if_pos)
        my_ast = ast.parse(source)

        visitor= ASTDotVisitor()
        visitor.visit(my_ast)