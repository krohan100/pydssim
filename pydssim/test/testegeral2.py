'''
Created on 20/04/2010

@author: Luiz Gustavo
'''

from datetime import datetime, timedelta

import time
import threading





if __name__ == '__main__':
    

    now = datetime.now()

    
    t1 =time.time()
    print time.asctime(time.localtime(t1))
    while (time.time() - t1) <60:
        pass
    print time.asctime(time.localtime(time.time()))
                
    
   
   