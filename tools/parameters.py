import glob
import os
from types import *

__all__ = ["io", "parameters"]

class io():
    def __init__(self, fileName, glob=None):
        self.fileName = fileName
        self.glob     = glob

    def getName(self):
        return self.fileName

    def getGlob(self):
        return self.glob

    def getFiles(self):
        if self.glob is not None:
            return glob(self.glob)
        else:
            return [self.fileName]

    def exists(self):
        for file in self.getFiles():
            if ( not os.path.exists(file) ):
                return False
        return True

    def getStats(self):
        stats = {}
        files = self.getFiles()
        stats['numfiles'] = len(files)
        stats['size']     = 0

        for file in files:
            stats['size'] += os.stat(file).st_size

        self.stats = stats
        return stats

    def __repr__(self):
        files = self.getFiles()
        res = "#FILES " + str(len(files))
        if self.exists():
            stats = self.getStats()
            res += " SIZE " + str(stats['size'])
        res += " " + " ".join(files)
        return res

class paramPair():
    def __init__(self):
        self.name  = ""
        self.value = ""
        self.type  = ""


class parameters():
    def __init__(self):
        self.pairs = []

    def add(self, pos, name, value, type):
        pair = [name, value, type]
        self.pairs[pos] = pair

    def append(self, name, value, type):
        #print " appending name " + str(name) + " value " + str(value) + " type " + str(type)
        pair       = paramPair()
        pair.name  = name
        pair.value = value
        pair.type  = type

        self.pairs.append(pair)


    def parse(self, name, type, dashes, equal, res):
        text    = ''
        if dashes is not None:
            text    = '-'*dashes
        text   += name

        if equal is True:
            text += '='
        if equal is False:
            text += ' '

        if res is not None:
            #print "APPENDING " + name + " RES " + str(res)
            self.append(text, res, type)
        else:
            #print "RES IS NONE FOR NAME " + str(name)
            #exit(1)
            pass


    def parseList(self, data, kwargs):
        for key in data.keys():
            values = data[key]
            #'buffer_size':     { 'name': 'buffer-size',     'type': 'num',  'dashes': 2, 'equal': True  },
            type   = values.get('type',   None)
            dashes = values.get('dashes', None)
            equal  = values.get('equal',  None)
            kkey   = key
            kkey   = kkey.replace("-", "_")
            kkey   = kkey.replace(".", "_")
            res    = kwargs.get(kkey,     None)
            self.parse(key, type, dashes, equal, res)

    def getCmd(self):
        pairs = self.pairs
        cmds  = []
        for pair in pairs:
            type  = pair.type
            name  = pair.name
            value = pair.value
            cmd   = ''
            
            if value is ListType:
                for el in value:
                    cmd = getLine(type, name, el)
                    cmds.append(cmd)
            elif value is FunctionType or value is InstanceType or value is MethodType:
                el  = value()
                cmd = getLine(type, name, el)
                cmds.append(cmd)
            else:
                cmd = self.getLine(type, name, value)
                cmds.append(cmd)
            
        return " ".join(cmds)

    def getLine(self, type, name, value):
        cmd = ""
        
        if   type == 'bool':
            cmd = name
        elif type == 'text':
            cmd = name + "'" + str(value) + "'"
        elif type == 'num':
            cmd = name + str(value)
        elif type == 'name':
            cmd = name
        elif type == 'value':
            cmd = value
        elif type == 'file':
            cmd = name + str(value)
        elif type == 'glob':
            cmd = name + str(value)
        elif type == 'fileList':
            cmd = name + " ".join(value)
        else:
            print "type " + str(type) + " is unknown"
        
        return cmd

    def hasParam(self, qry):
        for pair in self.pairs:
            if pair.name == qry:
                return True
        return False

    def getValue(self, qry):
        for pair in self.pairs:
            if pair.name == qry:
                return pair.value
        return False
