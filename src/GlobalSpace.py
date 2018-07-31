'''
Created on 2016年5月9日
@author: Casey-NS
'''

from src.Config import Config;
import threading;

mylock = threading.RLock()  
data_buffer = []


class GlobalSpace:
    
    CFG = Config()
    
#     mylock = threading.RLock()  
#     data_buffer = []
    
    def __init__(self):
        pass
    
    def append_data_buffer(self, dictV):
        global data_buffer
        global mylock
        
        mylock.acquire()
        data_buffer.append(dictV)
        mylock.release()
    
    def pop_data_buffer(self):
        global data_buffer
        global mylock
        
        mylock.acquire()
        pop_item = data_buffer.pop()
        mylock.release()    
        
        return pop_item