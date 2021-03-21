import os, sys
from functools import reduce

########################################################## generic input/output

def dir(args, env):
    for i in args:
        try: os.mkdir(i)
        except FileExistsError: pass

#################################################################### basic math

def add(ast, env):
    return reduce(lambda a, b: a + b, ast)

def sub(ast, env):
    return reduce(lambda a, b: a - b, ast)

def mul(ast, env):
    return reduce(lambda a, b: a * b, ast)

def div(ast, env):
    return reduce(lambda a, b: a / b, ast)

def pow(ast, env):
    return reduce(lambda a, b: a ^ b, ast)

############################################################ global environment


glob = {'type': 'env', 'value': 'global',
        '+': add, '-': sub, '*': mul, '/': div, '^': pow
        }

############################################################## core interpreter

class SpecialForm(NotImplementedError): pass

def eval(ast, env):
    if type(ast) in [None.__class__, int, str]: return ast
    if isinstance(ast, list):
        fn = ast[0]
        args = ast[1:]
        args = [eval(i, env) for i in args]
        return fn(args, env)
    raise NotImplementedError(ast)

def do(args, env): return args

def quote(ast, env): return ast

########################################################## read-eval-print-loop

def read(): raise NotImplementedError
# def print(exp): raise NotImplementedError('use system print')
def loop(): raise NotImplementedError

################################################### metacircular implementation


circ = [dir, 'circ']

all = [do, circ]

# print(eval(all, glob))

################################################################### system init

if __name__ == '__main__':
    if sys.argv[1] == 'all':
        print(eval(all, glob))
    else:
        raise SyntaxError(sys.argv)
