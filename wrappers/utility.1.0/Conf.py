#!/usr/bin/python
#-*- coding: UTF-8 -*-


import os, sys
from ConfigParser import ConfigParser

class Conf:
    def __init__(self, conffile):
        self.conffile = conffile
        self.config = ConfigParser()
        self.config.readfp(open(conffile))
       
    def getModules(self, conffile):
        if not conffile: conffile = self.conffile
        mod = {}
        i = 1
        while self.config.has_option('Modules', str(i)):
            try:
                mod[i] = self.config.get('Modules', str(i))
            except ConfigParser.NoOptionError, err:
                sys.exit('Conf.py -- NoOptionError -- %s' %err)
            i = i + 1
        return mod
        
    def getSection(self, section):
        mod = {}
        i = 1
        #print '\n',section
        for opt in self.config.options(section):
            #try:
                mod[opt] = self.config.get(section, opt)
                #print opt, self.config.get(section, opt)
            #except ConfigParser.NoOptionError, err:
                #sys.exit('Conf.py -- NoOptionError -- %s')# %err)
                i = i + 1
        return mod
    
    def getOptions(self, section):
        return self.config.options(section)
