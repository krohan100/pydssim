'''
Created on 22/08/2009

@author: LGustavo
'''

from pydssim.util.interface import implements

def return_type(type):
    def make_wrapper(f):
        def wrapper(*args, **kwargs):
            obj = f(*args, **kwargs)
            if obj:
                if hasattr(type, "implements"):
                    if not implements(obj, type):
                        raise TypeError, "Expected '%s' ; was %s." % (type, obj.__class__)
                elif not isinstance(obj, type):
                    raise TypeError, "Expected '%s' ; was %s." % (type, obj.__class__)
            return obj
        return wrapper
    return make_wrapper