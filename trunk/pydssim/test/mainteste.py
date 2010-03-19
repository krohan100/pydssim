'''
Created on 29/01/2010

@author: LGustavo
'''

import math
from portal import Portal
from peer import Peer

#
#
def find_key(dic, val):
    return dict([(k,v) for k, v in dic.iteritems() if v == val])#[0]


if __name__ == '__main__':
    #print math.log(5,2)
    #print math.trunc(math.log(5,2))
    portal = Portal()
   
   
    for i in range(1,5):
        peer = Peer(i)
        #portal.addSuperPeer(peer.getID(),peer.getLevelNeighbor())
        
        portal.addSuperPeer(peer)
        peer.discoverNewNeighbor(portal, portal.getDimension())
    
    print len(portal.getSuperPeers())
    
    '''    
    for k,v in portal.getSuperPeers().iteritems():
        print k,v 
   
   
    
    opp = portal.getPeers().pop(3)
    print opp
    
    
    print "max",max(portal.getSuperPeers().values())  
    print "mim",min(portal.getSuperPeers().values())
    
    
    for k in portal.getSuperPeers().values():
        print k
    
    
    '''
    #super = find_key(portal.getSuperPeers(), min(portal.getSuperPeers().values())) 
    #super = portal.getSuperPeerWithLevel(min(portal.getSuperPeers().values()))
    super = portal.getSuperPeers()
    print "con -> ",portal.getDimension()
    print "super" ,super 
    #for k,v in super.iteritems():
    #    print k,v    
       
        
        