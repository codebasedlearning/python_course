# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about Python's abstract syntax tree (ast).

Teaching focus
  - ast.parse
  - eval

References
  - https://docs.python.org/3/library/ast.html
  - https://docs.python.org/3/library/functions.html#eval
  - https://greentreesnakes.readthedocs.io/en/latest/tofrom.html
"""

import ast

from utils import print_function_header


# parse and then show ast-structure with 'dump'

@print_function_header
def use_ast_parse_and_dump():
    """ dumps ast-structure of a code-snippet """

    code = """
x=20+22
    """

    root = ast.parse(code)
    print(f" 1| {type(root)=}, {vars(root)=}, dump:")
    print(ast.dump(root, include_attributes=False, indent=4))

    body = root.body
    assign = root.body[0]
    print(f" 2| {type(body)=}, {type(assign)}, {vars(assign)=}, dump:")
    print(ast.dump(assign, include_attributes=False, indent=4))
    print()


@print_function_header
def ast_example_std_code():
    """ show ast-structure of a standard code-snippet """

    code = """
x = math.sin(1.0)
for i in range(1,5):
    print(f"... {i=}")
if x>0:
    y=1
else:
    y=2
    """

    root = ast.parse(code)
    print(f" 1| std code example, dump:")
    print(ast.dump(root, include_attributes=False, indent=4))
    print()


@print_function_header
def ast_example_class():
    """ show ast-structure of a class-code-snippet """

    code = """
class C:
    def f(self): self.x = 1
obj = C()
    """

    root = ast.parse(code)
    print(f" 1| class example, dump:")
    print(ast.dump(root, include_attributes=False, indent=4))
    print()


# it can also be executed...

@print_function_header
def run_it():
    """ run a code-snippet """

    code_exec = """
x=20+22
print(f" a| - {x=}")
        """
    root_exec = ast.parse(code_exec)
    exec(compile(root_exec, filename="<ast>", mode="exec"))         # there is 'exec' and 'eval'

    global_vars = {'y': 1}
    code_eval = """1 + 1/2 + y"""
    result = eval(code_eval, global_vars)   # set the environment
    print(f" 1| {result=}")


if __name__ == "__main__":
    use_ast_parse_and_dump()
    ast_example_std_code()
    ast_example_class()
    run_it()
