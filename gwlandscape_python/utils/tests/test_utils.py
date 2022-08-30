import pytest
from gwlandscape_python.utils import mutually_exclusive, _get_args_dict


@pytest.mark.parametrize("args,kwargs,args_dict", [
    ((1, 2), {'arg3': 3, 'arg4': 4}, {'arg1': 1, 'arg2': 2, 'arg3': 3, 'arg4': 4}),
    ((1, ), {'arg2': 2, 'arg3': 3, 'arg4': 4}, {'arg1': 1, 'arg2': 2, 'arg3': 3, 'arg4': 4}),
    ((), {'arg1': 1, 'arg2': 2, 'arg3': 3, 'arg4': 4}, {'arg1': 1, 'arg2': 2, 'arg3': 3, 'arg4': 4}),
    ((1, 2, 3, 4), {}, {'arg1': 1, 'arg2': 2, 'arg3': 3, 'arg4': 4}),
    ((1, 2, 3), {}, {'arg1': 1, 'arg2': 2, 'arg3': 3}),
    ((1, 2), {'arg4': 4}, {'arg1': 1, 'arg2': 2, 'arg4': 4}),
    ((1, 2), {}, {'arg1': 1, 'arg2': 2}),
])
def test_get_args_dict(args, kwargs, args_dict):
    def arbitrary_func(arg1, arg2, arg3=None, arg4=None):
        return True

    assert _get_args_dict(arbitrary_func, args, kwargs) == args_dict


@pytest.fixture
def get_mutex_func():
    def mutex_func(*mutex_args):
        @mutually_exclusive(*mutex_args)
        def arbitrary_func(arg1=None, arg2=None, arg3=None, arg4=None):
            return True

        return arbitrary_func
    return mutex_func


@pytest.mark.parametrize("mutex_args,args_dict", [
    (('arg1', 'arg2'), {'arg1': 1, 'arg2': 2}),
    (('arg1', 'arg2', 'arg3'), {'arg1': 1, 'arg2': 2}),
    (('arg1', 'arg2', 'arg3'), {'arg1': 1, 'arg3': 3}),
    (('arg1', 'arg2', 'arg3'), {'arg2': 2, 'arg3': 3}),
    (('arg1 | arg2', 'arg3'), {'arg1': 1, 'arg3': 3}),
    (('arg1 | arg2', 'arg3'), {'arg2': 2, 'arg3': 3}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg1': 1, 'arg3': 3}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg1': 1, 'arg4': 4}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg2': 2, 'arg3': 3}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg2': 2, 'arg4': 4}),
    (('arg1 | arg2 | arg3', 'arg4'), {'arg1': 1, 'arg4': 4}),
    (('arg1 | arg2 | arg3', 'arg4'), {'arg2': 2, 'arg4': 4}),
    (('arg1 | arg2 | arg3', 'arg4'), {'arg3': 3, 'arg4': 4}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg1': 1, 'arg2': 2}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg1': 1, 'arg3': 3}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg1': 1, 'arg4': 4}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg2': 2, 'arg3': 3}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg2': 2, 'arg4': 4}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg3': 3, 'arg4': 4}),
])
def test_mutually_exclusive_fail(get_mutex_func, mutex_args, args_dict):
    func = get_mutex_func(*mutex_args)
    with pytest.raises(SyntaxError):
        func(**args_dict)


@pytest.mark.parametrize("mutex_args,args_dict", [
    (('arg1', 'arg2'), {'arg1': 1}),
    (('arg1', 'arg2'), {'arg2': 2}),
    (('arg1', 'arg2'), {'arg3': 3}),
    (('arg1', 'arg2'), {'arg1': 1, 'arg3': 3}),
    (('arg1', 'arg2'), {'arg2': 2, 'arg3': 3}),
    (('arg1', 'arg2', 'arg3'), {'arg1': 1, 'arg4': 4}),
    (('arg1', 'arg2', 'arg3'), {'arg2': 2, 'arg4': 4}),
    (('arg1', 'arg2', 'arg3'), {'arg3': 3, 'arg4': 4}),
    (('arg1 | arg2', 'arg3'), {'arg1': 1, 'arg4': 4}),
    (('arg1 | arg2', 'arg3'), {'arg2': 2, 'arg4': 4}),
    (('arg1 | arg2', 'arg3'), {'arg3': 3, 'arg4': 4}),
    (('arg1 | arg2', 'arg3'), {'arg1': 1, 'arg2': 2}),
    (('arg1 | arg2', 'arg3'), {'arg1': 1, 'arg2': 2, 'arg4': 4}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg1': 1}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg2': 2}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg3': 3}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg4': 4}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg1': 1, 'arg2': 2}),
    (('arg1 | arg2', 'arg3 | arg4'), {'arg3': 3, 'arg4': 4}),
    (('arg1 | arg2 | arg3', 'arg4'), {'arg1': 1, 'arg2': 2}),
    (('arg1 | arg2 | arg3', 'arg4'), {'arg1': 1, 'arg3': 3}),
    (('arg1 | arg2 | arg3', 'arg4'), {'arg2': 2, 'arg3': 3}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg1': 1}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg2': 2}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg3': 3}),
    (('arg1', 'arg2', 'arg3', 'arg4'), {'arg4': 4}),
])
def test_mutually_exclusive_succeed(get_mutex_func, mutex_args, args_dict):
    func = get_mutex_func(*mutex_args)
    assert func(**args_dict)
