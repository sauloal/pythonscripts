class parameters():
    def __init__(self):
        self.pairs = []
        self.cmd   = []

    class paramPair():
        def __init__(self):
            self.name  = ""
            self.value = ""
            self.type  = ""
            self.cmd   = ""


    def add(self, pos, name, value, type):
        pair = [name, value, type]
        self.pairs[pos] = pair

    def append(self, name, value, type):
        #print " appending name " + str(name) + " value " + str(value) + " type " + str(type)
        pair       = self.paramPair()
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
        else:
            print "type " + str(type) + " is unknown"

        self.pairs.append(pair)
        self.cmd.append(pair.cmd)


    def parse(self, name, type, dashes, equal, res):
        text    = '-'*dashes
        text   += name

        if equal is True:
            text += '='
        if equal is False:
            text += ' '
        else:
            text += ''

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
            name   = values.get('name',   None)
            type   = values.get('type',   None)
            dashes = values.get('dashes', None)
            equal  = values.get('equal',  None)
            res    = kwargs.get(key,      None)
            self.parse(name, type, dashes, equal, res)

    def getCmd(self):
        return " ".join(self.cmd)

