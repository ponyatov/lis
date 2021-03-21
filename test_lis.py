def test_true(): assert True


from lis import *

def test_math_add_mul():
    ast = [glob['+'], 2, [glob['*'], 3, 4]]
    assert ast == [add, 2, [mul, 3, 4]]
    assert eval(ast, glob) == 14

def test_math_sub_div():
    ast = [glob['-'], 2, [glob['/'], 3, 4]]
    assert ast == [sub, 2, [div, 3, 4]]
    assert eval(ast, glob) == 1.25
