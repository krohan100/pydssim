'''
Created on 22/08/2009

@author: LGustavo
'''

from random import randint
from pydssim.util.resource_maps import *
from pydssim.util.logger import *
from time import ctime
from pydssim.peer.resource.hardware_resource import Hardware 
import uuid

def get():    
    op = [ServiceMap(),HardwareMap()]
    for i in range(0,3):
        resources = ResourceMap(op[randint(0,1)])
     
        map = resources.Map()
        concept = map.keys()[randint(0, len(map.keys()) - 1)]
        initial = randint(0, (len(map[concept])/2) - 1)
        end = randint((len(map[concept])/2), len(map[concept]) - 1)
        print 'id %d conce %s indtial %d End %d' % (i,concept,initial,end)  
        
        for ix in range(initial, end):
            print map[concept][ix] 

if __name__ == '__main__':
    my = Logger()
    my.resgiterLoggingError("Star Simulation")
    m2 = Logger('w')
    m2.resgiterLoggingInfo("Star Simulation2")
    # Obtm um datatime da data e hora atual
    hoje = datetime.today()
    print ctime() 
    h = Hardware(1,"memoria")
   
    print h.getPID(), h.getUUID()
    #get()    
  
        
    '''
    map = FolksonomyMap()
     
    id = 1  
    concept = map.mapping.keys()[randint(0, len(map.mapping.keys()) - 1)]
    initial = randint(0, (len(map.mapping[concept])/2) - 1)
    end = randint((len(map.mapping[concept])/2), len(map.mapping[concept]) - 1)
    print 'id %d conce %s indtial %d End %d' % (id,concept,initial,end)  
    
    for ix in range(initial, end):
        print map.mapping[concept][ix]

    ''' 
