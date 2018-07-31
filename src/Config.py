'''
Created on 2016年5月9日
@author: Casey-NS
'''

import configparser

class Config(object):
    
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read("config.conf")