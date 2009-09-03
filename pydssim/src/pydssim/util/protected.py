'''
Created on 22/08/2009

@author: LGustavo
'''

class Protected(object):
    '''
    Base class of all classes that want to hide protected attributes from
    public access.
    '''
    def __new__(cls, *args, **kwd):
        obj = object.__new__(cls)        
        cls.__init__(obj, *args, **kwd)
                                
        def __getattr__(self, name):            
            attr = getattr(obj, name)
            if hasattr(attr, "__public__"):
                return attr
            elif hasattr(cls, "__public__"):
                if name in cls.__public__:
                    return attr                            
            raise AttributeError, "Attribute %s is not public."%name
        
        def __setattr__(self, name, value):
            attr = getattr(obj, name)                
            cls.__setattr__(self, name, value)    

        # Magic methods defined by cls must be copied to Proxy.
        # Delegation using __getattr__ is not possible.

        def is_own_magic(cls, name, without=[]):
            return name not in without and\
                   name.startswith("__") and name.endswith("__")

        #Proxy = type("Protected(%s)"%cls.__name__,(),{})   
        Proxy = type("Protected(%s)"%cls.__name__,(),{})
        for name in dir(cls):
            if is_own_magic(cls,name, without=dir(Proxy)):
                try:
                    setattr(Proxy, name, getattr(obj,name))
                except TypeError:
                    pass
                    
        
        Proxy.__getattr__ = __getattr__
        Proxy.__setattr__ = __setattr__
        return Proxy()

        