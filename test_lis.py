def test_true(): assert True


from lis import *

def test_math_add_mul():
    ast = [math['+'], 2, [math['*'], 3, 4]]
    assert ast == [add, 2, [mul, 3, 4]]
    assert eval(ast, math) == 14

def test_math_sub_div():
    ast = [math['-'], 2, [math['/'], 3, 4]]
    assert ast == [sub, 2, [div, 3, 4]]
    assert eval(ast, math) == 1.25

def test_env_get():
    assert glob['/'] == div

def test_env_set():
    assert 'test_env_set' not in glob.keys()
    glob['test_env_set'] = test_env_set
    assert glob['test_env_set'] == glob['test_env_set']
