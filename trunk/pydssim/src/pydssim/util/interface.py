'''
Created on 22/08/2009

@author: LGustavo
'''

class Interface(type):
    """The Interface metaclass."""

    def __init__(cls, name, bases, dct):
        super(Interface, cls).__init__(name, bases, dct)
        attribs = dct.keys()
        #Remove __metaclass__.
        attribs.remove('__metaclass__')
        #Store declared attributes => call super setattr.
        super(Interface, cls).__setattr__('__attributes__', attribs)

    #interfaces are "static" objects => we disallow dynamic changes.
    def __setattr__(cls, name, value):
        raise AttributeError("Cannot bind attributes in interface classes.")

    def __delattr__(cls, name):
        raise AttributeError("Cannot delete attributes in interface classes.")

    def attributes(cls):
        """Returns the list of noncallable attributes's names."""
        #Get mro list of interfaces.
        interfaces = [interface for interface in cls.mro() \
                      if isinstance(interface, Interface)]
        #Build list of attribs.
        attribs = {}
        for interface in interfaces:
            for attrib in interface.__attributes__:
                if not callable(getattr(interface, attrib)):
                    attribs[attrib] = None
        return attribs.keys()

    def callables(cls):
        """Returns the list of callable attributes's names."""
        #Get mro list of interfaces.
        interfaces = [interface for interface in cls.mro() \
                      if isinstance(interface, Interface)]
        #Build list of attribs.
        attribs = {}
        for interface in interfaces:
            for attrib in interface.__attributes__:
                if callable(getattr(interface, attrib)):
                    attribs[attrib] = None
        return attribs.keys()

    def implements(cls, obj):
        """Returns 1 if obj implements interface cls, 0 otherwise."""
        #Check attributes.
        for attrib in cls.attributes():
            try:
                objattrib = getattr(obj, attrib)
            except AttributeError:
                return 0
            else:
                if callable(objattrib):
                    return 0
        #Check callables.
        for attrib in cls.callables():
            try:
                objattrib = getattr(obj, attrib)
            except AttributeError:
                return 0
            else:
                if not callable(objattrib):
                    return 0
        return 1
