# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet is about modifying an ast.
"""

import ast


# modify an ast? yes... but why?

class ExampleVisitor(ast.NodeVisitor):

    # tiny indent control
    _indent = 0
    @classmethod
    def indent(cls): return ' '*cls._indent

    @classmethod
    def inc_indent(cls): cls._indent += 2

    @classmethod
    def dec_indent(cls): cls._indent -= 2

    # modify all nodes you are interested in

    def visit_Constant(self, node):
        print(f"{ExampleVisitor.indent()}CONST {node.value}")
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node):
        print(f"{ExampleVisitor.indent()}CALL '{node.func.attr}' with")
        ExampleVisitor.inc_indent()
        self.generic_visit(node)
        ExampleVisitor.dec_indent()

    def visit_Assign(self, node):
        print(f"{ExampleVisitor.indent()}ASSIGN {node.targets[0].id}")
        ExampleVisitor.inc_indent()
        self.generic_visit(node)
        ExampleVisitor.dec_indent()

    def visit_If(self, node):
        print(f"{ExampleVisitor.indent()}IF <condition>")
        if_node = node.body
        if if_node:
            ExampleVisitor.inc_indent()
            self.generic_visit(if_node[0])                          # specific for the example, not general
            ExampleVisitor.dec_indent()

        else_node = node.orelse
        if else_node:
            print(f"{ExampleVisitor.indent()}ELSE")
            ExampleVisitor.inc_indent()
            self.generic_visit(else_node[0])                        # specific for the example, not general
            ExampleVisitor.dec_indent()


def visit_nodes():
    """ visit nodes of an ast and dump the structure """
    print("\nvisit_nodes\n===========")

    code = """
x = math.sin(1.0)
if x>0:
    y=1
else:
    y=2
"""

    root = ast.parse(code)
    print(f" 1| visit nodes, dump:")
    print(ast.dump(root, indent=4))

    print(f" 2| now visit:")
    visitor = ExampleVisitor()
    visitor.visit(root)
    print()


# as an idea: replace calls to an 'old' library with new ones, e.g. with different args such that
# 'monkey patching' does not work out-of-the-box

class NewLib:
    @staticmethod
    def new_connect(name):
        print(f" a| -> new_connect('{name}')")


class LibConnectionMock(ast.NodeTransformer):

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.value.id == 'lib' and node.func.attr == 'connect':
            new_node = ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id='NewLib', ctx=ast.Load()),
                    attr='new_connect',
                    ctx=ast.Load()),
                args=node.args,                                     # could be changed to new args
                keywords=node.keywords)
            ast.copy_location(new_node, node)
            ast.fix_missing_locations(new_node)                     # set lineno and col_offset
            return new_node
        return node


def modify_nodes():
    """ modify nodes of an ast and dump the structure """
    print("\nmodify_nodes\n============")

    code = """
db = lib.connect('url')
"""

    root = ast.parse(code)
    print(f" 1| modify nodes, dump original:")
    print(ast.dump(root, indent=4))

    LibConnectionMock().visit(root)
    print(f" 2| dump mocked:")
    print(ast.dump(root, indent=4))
    print(f" 3| exec:")
    exec(compile(root, filename="<ast>", mode="exec"))


if __name__ == "__main__":
    visit_nodes()
    modify_nodes()


"""
https://docs.python.org/3/library/ast.html
https://greentreesnakes.readthedocs.io/en/latest/index.html
https://gist.github.com/jtpio/cb30bca7abeceae0234c9ef43eec28b4
"""
