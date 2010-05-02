'''
Created on 20/04/2010

@author: Luiz Gustavo
'''
from datetime import datetime
import threading





if __name__ == '__main__':
    

    dic_1 = {'a':10,'c':03,'b':02}

    dic_aux = dic_1
    print dic_1
    dic_aux = sorted(dic_aux)
    
    print dic_aux
    dic_resultado = {}

    for item in sorted(dic_1):
        print item
        dic_resultado[item] = dic_1[item]
    
    print dic_resultado
                
    
   
   