import warnings
from functools import wraps


# Taken from https://stackoverflow.com/a/40363565
# Needed to be able to identify the names of arguments provided,
# whether or not they were positional or keywords
def _get_args_dict(fn, args, kwargs):
    args_names = fn.__code__.co_varnames[:fn.__code__.co_argcount]
    return {**dict(zip(args_names, args)), **kwargs}


# Heavily adapted from https://stackoverflow.com/a/54487188
def mutually_exclusive(*keywords):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if not keywords:
                warnings.warn('mutually_exclusive decorator does nothing without arguments', SyntaxWarning)

            arg_list = _get_args_dict(func, args, kwargs)

            # Split OR groups, and then count how many of the mutually exclusive keywords appear in the the kwargs
            keyword_sets = [keyword.replace(' ', '').split('|') for keyword in keywords]
            n_mutex_keywords = sum(any(k in arg_list for k in keyword_set) for keyword_set in keyword_sets)

            # If there is more than one of the mutually exclusive arguments, we have a problem
            if n_mutex_keywords > 1:
                raise SyntaxError('You must specify at most one of {}'.format(', '.join(keywords)))

            return func(*args, **kwargs)
        return inner
    return wrapper
