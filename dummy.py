def actual_kwargs():
    """
    Decorator that provides the wrapped function with an attribute 'actual_kwargs'
    containing just those keyword arguments actually passed in to the function.
    """
    def decorator(function):
        def inner(*args, **kwargs):
            inner.actual_kwargs = kwargs
            return function(*args, **kwargs)
        return inner
    return decorator

@actual_kwargs()
def s(a=1,b=2, **kwargs):
	print(s.actual_kwargs)

s(c=3)