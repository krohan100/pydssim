'''
Created on 22/08/2009

@author: LGustavo
'''

def public(f):
    '''
    Decorator used to assign the attribute __public__ to methods.
    '''
    f.__public__ = True
    return f
