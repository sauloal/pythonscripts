import glob, os, sys
from types import *

__all__ = ["io", "parameters"]

class io():
    def __init__(self, fileName):
        print " IO :: FN " + str(fileName)
        self.fileName = fileName

    def getFileName(self):
        return self.fileName

    def getFiles(self):
        files = []
        
        if type(self.fileName) in StringTypes:
            print "string type"
            files = glob.glob(self.fileName)

        elif type(self.fileName) is ListType:
            print "list type"
            files = self.fileName
        
        files = decovolute(files)

        filesOut = []
        for file in files:
            if file is not None:
                print " CHEKING FILE " + str(file)
                if not os.path.exists(file):
                    print " FILE " + file + " DOES NOT EXISTS"
            else:
                print " FILE IN FILES " + str(files) + " IS NONE"
                sys.exit(1)

            fileReal = os.path.abspath(os.path.realpath(os.path.normpath(file)))

            if not os.path.isfile(fileReal):
                print " INPUT FILE " + file + " ("+fileReal+") IS NOT A FILE"
            else:
                print " INPUT FILE " + file + " ("+fileReal+") IS A FILE"
            
            print " INPUT FILE " + file + " ("+fileReal+") APPENDING"
            filesOut.append(fileReal)

        return filesOut

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
        #print str(files)
        #print self.fileName
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
            ptype  = pair.type
            name   = pair.name
            value  = pair.value
            cmd    = ''

            valueF = decovolute(value)
            #print "  VALUE F " + str(valueF)
            cmd    = self.getLine(ptype, name, valueF)
            #print "  CMD     " + str(cmd)
            cmds.append(cmd)
            
        #print " CMDS " + str(cmds)
        return " ".join(cmds)


    def getLine(self, ptype, name, value):
        cmd = ""

        if type(value) is ListType:
            #print " GETLINE LIST " + str(value)
            tmpval = ""
            for val in value:
                if tmpval != "":
                    tmpval += " "
                tmpval += str(val)
            value = tmpval
            #print " GETLINE LIST VALUE FINAL " + str(value)
            
        if   ptype == 'bool':
            cmd = name
        elif ptype == 'text':
            cmd = name + "'" + str(value) + "'"
        elif ptype == 'num':
            cmd = name + str(value)
        elif ptype == 'name':
            cmd = name
        elif ptype == 'value':
            cmd = value
        elif ptype == 'file':
            cmd = name + value
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


def decovolute(value):
    cmds = []
    
    if type(value) is ListType:
        #print "VALUE " + str(value) + " IS LIST " + str(type(value))
        for el in value:
            if el in StringTypes:
                cmds.append(el)
            else:
                cmd = decovolute(el)
                cmds.extend(cmd)

    elif type(value) in StringTypes:
        #print "VALUE " + str(value) + " IS STRING " + str(type(value))
        cmds.append(value)

    elif isinstance(value, io):
        #print "VALUE " + str(value) + " IS IO INSTANCE " + str(type(value))
        cmds.extend(decovolute(value.getFiles()))

    elif type(value) in (FunctionType, InstanceType, MethodType):
        #print "VALUE " + str(value) + " IS FUNCTION " + str(type(value))
        cmd  = value()
        cmds.extend(decovolute(cmd))

    else:
        #print "UNKNOWN TYPE TO DECOVOLUTE " + str(type(value))
        cmds.append(value)
    
    #print "CMDS DEC " + str(cmds)
    return cmds