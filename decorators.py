## Decorators for FTLite ##

def returnFunc(func):
    """A decorator that modifies the behavior of a function f(*args, **kwargs)
	to return another function object g such that a call to g() has the same
	behavior as a call to f(*args, **kwargs) would have had as f was originally defined
    """
    def newBehavior(*args, **kwargs):
        def functionObject():
            func(*args, **kwargs)
        return functionObject
    return newBehavior

        
    

    