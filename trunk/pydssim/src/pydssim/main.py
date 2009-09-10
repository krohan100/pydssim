'''
Created on Sep 10, 2009

@author: gustavo
'''


from random import randint
from pydssim.util.resource_maps import *
from pydssim.util.logger import *
from time import ctime
from pydssim.peer.resource.hardware_resource import Hardware 
from pydssim.peer.resource.abstract_resource import AbstractResource
from pydssim.peer.resource.service_resource import Service
from pydssim.peer.repository.service_repository import ServiceRepository
from pydssim.util.protected import Protected
import uuid

def teste(t1=uuid.uuid1(),t2='',t3="t3",t4="t4"):
    print t1,t2,t3,t4

def get(tam=3):    
    opmap   = [ServiceMap(),HardwareMap()]
    opclass = [Service(),Hardware()]
    opclassd = {'1':1,'2':2}
    for i in range(0,tam):
        op = randint(0,1)
        resourceMap = ResourceMap(opmap[op])
     
        map = resourceMap.Map()
        concept = map.keys()[randint(0, len(map.keys()) - 1)]
        initial = randint(0, (len(map[concept])/2) - 1)
        end = randint((len(map[concept])/2), len(map[concept]) - 1)
        print opclassd.keys()[op]
        print 'id %d conce %s indtial %d End %d' % (i,concept,initial,end)  
        
        for ix in range(initial, end):
            service = opclass[op]
            #print service.getUUID()
            print map[concept][ix] 

if __name__ == '__main__':
    
    # teste(t2="teste2",t4="teste4")
    get(1)