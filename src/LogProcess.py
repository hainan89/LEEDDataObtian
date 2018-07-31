# import random
# import time
# import logging
from src.GlobalSpace import GlobalSpace;
import logging.handlers
import time

class LogProcess(GlobalSpace):
    """ simulate the action of the browser"""
    
    def __init__(self, log_name_str):
        
        log_level = {"Debug":logging.DEBUG, "Info":logging.INFO, "Warning":logging.WARNING,
                     "Error":logging.ERROR, "Critical":logging.CRITICAL}
        
        log_name_str = "{0}-{1}".format(log_name_str, time.time())
        
        # loging system configuring
        self.logger = logging.getLogger(log_name_str)
        self.logger.setLevel(log_level[self.CFG.cf["log"]["log_level"]])
         
        self.LOG_FILE = 'logs/{0}.log'.format(log_name_str)
        
        self.fh = logging.handlers.RotatingFileHandler(self.LOG_FILE, maxBytes = 1024*1024, backupCount = 5, encoding='utf-8')  
        self.fh.setLevel(logging.DEBUG)
        
        self.ch = logging.StreamHandler()  
        self.ch.setLevel(logging.DEBUG)  
        
        fmt = '%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)s - %(message)s'
        formatter = logging.Formatter(fmt)   # 实例化formatter  
        self.fh.setFormatter(formatter)      # 为handler添加formatter
        self.ch.setFormatter(formatter)      # 为handler添加formatter
        
        self.logger.addHandler(self.fh)           # 为logger添加handler  
        self.logger.addHandler(self.ch)           # 为logger添加handler
        
#         return self.logger
        #end of the __init__

    def init(self, log_name_str):
        log_name_str = "{0}-{1}".format(log_name_str, time.time())
        
        # loging system configuring
        self.logger = logging.getLogger(log_name_str)
        self.logger.setLevel(logging.DEBUG)
         
        self.LOG_FILE = 'logs/{0}.log'.format(log_name_str)
        
        self.fh = logging.handlers.RotatingFileHandler(self.LOG_FILE, maxBytes = 1024*1024, backupCount = 5, encoding='utf-8')  
        self.fh.setLevel(logging.DEBUG)
        
        self.ch = logging.StreamHandler()  
        self.ch.setLevel(logging.DEBUG)  
        
        fmt = '%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)s - %(message)s'
        formatter = logging.Formatter(fmt)   # 实例化formatter  
        self.fh.setFormatter(formatter)      # 为handler添加formatter
        self.ch.setFormatter(formatter)      # 为handler添加formatter
        
        self.logger.addHandler(self.fh)           # 为logger添加handler  
        self.logger.addHandler(self.ch)           # 为logger添加handler
        
        return self.logger
        #end of the init
    
    
    
"""end class"""