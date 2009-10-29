'''
Created on 22/08/2009

@author: LGustavo
'''
from pydssim.util.protected import Protected
from pydssim.util.decorator.public import public
from pydssim.util.singleton import singleton
from datetime import datetime
import logging


class Logger(Protected):
    '''
    Class for logging
    '''
    
    #__metaclass__ = singleton
    
    
    def __init__(self,fileMode='w'):
        
        self.initialize(fileMode)
    
    def initialize(self,fileMode='w'):
        #today = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        #LOG_FILENAME = 'logging_simulatorfile_'+today+'.log'
        LOG_FILENAME = 'logging_simulation_file.log'
        logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=LOG_FILENAME,
                    filemode=fileMode)
        self.logger = logging.getLogger("pydssim")
        
    @public
    def resgiterLoggingInfo(self, msg):
        self.logger.info(msg)     
    
    @public
    def resgiterLoggingError(self, msg):
        self.logger.error(msg) 
        
        
