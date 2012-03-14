import glob
import os

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
        stats['numfiles'] = length(files)
        stats['size']     = 0

        for file in files:
            stats['size'] += os.stat(file).st_size

        self.stats = stats
        return stats

    def __repr__(self):
        stats = self.getStats()
        files = self.getFiles()
        print "#FILES " + stats['numfiles'] + " SIZE " + stats['size'] + " ".join(files)

class paramPair():
    def __init__(self):
        self.name  = ""
        self.value = ""
        self.type  = ""
        self.cmd   = ""


class parameters():
    def __init__(self):
        self.pairs = []
        self.cmd   = []

    def add(self, pos, name, value, type):
        pair = [name, value, type]
        self.pairs[pos] = pair

    def append(self, name, value, type):
        #print " appending name " + str(name) + " value " + str(value) + " type " + str(type)
        pair       = paramPair()
        pair.name  = name
        pair.value = value
        pair.type  = type

        if   type == 'bool':
            pair.cmd = name
        elif type == 'text':
            pair.cmd = name + "'" + str(value) + "'"
        elif type == 'num':
            pair.cmd = name + str(value)
        elif type == 'name':
            pair.cmd = name
        elif type == 'value':
            pair.cmd = value
        elif type == 'file':
            pair.cmd = name + str(value)
        elif type == 'glob':
            pair.cmd = name + str(value)
        elif type == 'fileList':
            pair.cmd = name + " ".join(value)
        else:
            print "type " + str(type) + " is unknown"

        self.pairs.append(pair)
        self.cmd.append(pair.cmd)


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
        return " ".join(self.cmd)

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
