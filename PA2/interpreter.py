import sys
from lark import Lark, Transformer, Tree
import lark
import os

#print(f"Python version: {sys.version}")
#print(f"Lark version: {lark.__version__}")

# run/execute/interpret source code
def interpret(source_code):
    cst = parser.parse(source_code)
    ast = LambdaCalculusTransformer().transform(cst)
    result_ast = evaluate(ast)
    result = linearize(result_ast)
    return result

# convert concrete syntax to CST
parser = Lark(open("grammar.lark").read(), parser='lalr')

# convert CST to AST
class LambdaCalculusTransformer(Transformer):
    def lam(self, args):
        name, body = args
        return ('lam', str(name), body)

    def app(self, args):
        return ('app', *args)

    def var(self, args):
        token, = args
        return ('var', str(token))

    def NAME(self, token):
        return str(token)

# reduce AST to normal form
def evaluate(tree):
    if tree[0] == 'app':
        e1 = evaluate(tree[1])
        if e1[0] == 'lam':
            body = e1[2]
            name = e1[1]
            arg = tree[2]
            rhs = substitute(body, name, arg) 
            return evaluate(rhs)
        else:
            # add e2
            e2 = evaluate(tree[2])
            return ('app', e1, e2)
    elif tree[0] == 'lam':
        return ('lam', tree[1], evaluate(tree[2]))
    else:
        return tree

# generate a fresh name 
# needed eg for \y.x [y/x] --> \z.y where z is a fresh name)
class NameGenerator:
    def __init__(self):
        self.counter = 0

    def generate(self):
        self.counter += 1
        return 'Var' + str(self.counter)

name_generator = NameGenerator()

# for beta reduction (capture-avoiding substitution)
# 'replacement' for 'name' in 'tree'
def substitute(tree, name, replacement):
    if tree[0] == 'var':
        if tree[1] == name:
            return replacement
        else:
            return tree
    elif tree[0] == 'lam':
        if tree[1] == name:
            return tree
        else:
            fresh_name = name_generator.generate()
            return ('lam', fresh_name,
                    substitute(substitute(tree[2], tree[1], ('var', fresh_name)),
                               name, replacement))
    elif tree[0] == 'app':
        return ('app', substitute(tree[1], name, replacement),
                      substitute(tree[2], name, replacement))
    else:
        raise Exception('Unknown tree', tree)


def linearize(ast):
    if ast[0] == 'var':
        return ast[1]
    elif ast[0] == 'lam':
        return "(" + "\\" + ast[1] + "." + linearize(ast[2]) + ")"
    elif ast[0] == 'app':
        return "(" + linearize(ast[1]) + " " + linearize(ast[2]) + ")"
    else:
        return str(ast)

def main():
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py <filename or expression>", file=sys.stderr)
        sys.exit(1)

    input_arg = sys.argv[1]

    if os.path.isfile(input_arg):
        with open(input_arg, 'r') as file:
            expression = file.read()
    else:
        expression = input_arg

    result = interpret(expression)
    print(f"\033[95m{result}\033[0m")

if __name__ == "__main__":
    main()
