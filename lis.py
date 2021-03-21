import os, sys
from functools import reduce

################################################################### object core

class Object:
    def __init__(self, V):
        self.value = V
        self.slot = {}
        self.nest = []

    def __repr__(self): return self.head()

    def pad(depth): return '\n' + '\t' * depth

    def dump(self, depth=0, prefix=''):
        # head
        ret = Object.pad(depth) + self.head(prefix)
        # slot{}s
        for i in self.keys():
            item = self[i]
            if isinstance(item, Object):
                ret += self[i].dump(depth + 1, f'{i} = ')
            else:
                ret += f'{Object.pad(depth+1)}{i} = {item}'
        # nest[]ed
        for j, k in enumerate(self.nest):
            ret += k.dump(depth + 1, f'{j}: ')
        # subtree
        return ret

    def head(self, prefix=''): return f'{prefix}{self.tag()}:{self.val()}'
    def tag(self): return self.__class__.__name__.lower()
    def val(self): return f'{self.value}'

    def keys(self):
        return sorted(self.slot.keys())

    def __floordiv__(self, that):
        assert isinstance(that, Object)
        self.nest += [that]; return self


########################################################## generic input/output

class Dir(Object):
    def __truediv__(self, that):
        if isinstance(that, str): that = Dir(that)
        assert isinstance(that, Dir)
        that.value = f'{self.value}/{that.value}'
        self // that
        try: os.mkdir(that.value)
        except FileExistsError: pass
        return self

def dir(args, env):
    assert len(args) == 1
    return Dir(args[0])
    # try: os.mkdir(args[0])
    # except FileExistsError: pass

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

############################################################# AST manipulations

# def push(ast, env):
#     return reduce(lambda a, b: a // b, ast)

############################################################ global environment

class Env(Object):
    def __init__(self, V, par=None, init={}):
        super().__init__(V)
        self.par = par
        self.slot = init

    def __getitem__(self, key):
        assert isinstance(key, str)
        try:
            return self.slot[key]
        except KeyError:
            if self.par:
                return self.par[key]
            else:
                raise KeyError([self, key])

    def __setitem__(self, key, that):
        assert isinstance(key, str)
        self.slot[key] = that; return self


glob = Env('global', init={
    '+': add, '-': sub, '*': mul, '/': div, '^': pow,
    # '//': push, #'<<': shl, '>>': shr
})

math = Env('math', par=glob)

############################################################## core interpreter

class SpecialForm(NotImplementedError): pass

def eval(ast, env):
    if type(ast) in [None.__class__, int, str]: return ast
    if isinstance(ast, list):
        fn = ast[0]
        args = ast[1:]
        if fn not in [quote]:
            args = [eval(i, env) for i in args]
        return fn(args, env)
    raise NotImplementedError(ast)

def do(ast, env): return ast
def quote(ast, env): return ast

########################################################## read-eval-print-loop

def read(): raise NotImplementedError
def loop(): raise NotImplementedError

# def print(exp): raise NotImplementedError('use dump() or system print()')
def dump(ast, env=glob, depth=0):
    def pad(depth): return Object.pad(depth)
    ret = ''
    if type(ast) in [None.__class__, int, str]:
        ret += f'{pad(depth)}{ast}'
    elif isinstance(ast, Object):
        ret += ast.dump(depth)
    elif isinstance(ast, list):
        ret += f'{pad(depth)}['
        for i in ast: ret += dump(i, env, depth + 1)
        ret += f'{pad(depth)}]'
    else:
        raise TypeError([type(ast), ast])
    if depth: return ret
    else: print(ret)


dump(glob)


################################################### metacircular implementation


circ = [dir, 'circ']

bin = [dir, 'bin']
doc = [dir, 'doc']
tmp = [dir, 'tmp']

# dirs = [glob['/'], circ, bin, doc, tmp]
dirs = [do, 1, [glob['/'], circ, 'bin', doc, tmp], 3]

################################################################### system init

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == 'all':
        print(eval(dirs, glob))
    else:
        raise SyntaxError(sys.argv)
