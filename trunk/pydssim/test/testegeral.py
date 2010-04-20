'''
Created on 20/04/2010

@author: Luiz Gustavo
'''

if __name__ == '__main__':
    teste = {}
    teste["001"] = (10,"Danielle")
    teste["002"] = {}
    
    
    
    teste["002"][0] = (10,"leticia")
    teste["002"][1] = (10,"clara")

    x,y = teste["002"][0]
    
    print teste["002"].keys(), teste.values()
    print x,y