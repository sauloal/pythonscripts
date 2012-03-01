if __name__ == "__main__":
    import os
    import sys

    fullpath=os.getcwd()

    #print "CURRENT PATH " + fullpath
    fullpath=os.path.abspath(fullpath + "/..")
    #print "PREVIOUS PATH " + fullpath
    sys.path.append(fullpath)
    #print "PATH " + str(sys.path)

from tools import *

#http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python

class sampleWrapper():
    def __init__(self, name):
        self.name       = name
        self.exitStatus = 255 #not run

    def sample(self, writeOut, writeErr, status, err):
        self.status     = status
        self.err        = err
        self.writeOut   = writeOut
        self.writeErr   = writeErr

        print "RUNNING WRAPPER NAMED " + self.name
        self.status = joblaunch.FINISH
        print "GOT STATUS " + str(status) + " RETURNIN STATUS " + str(self.status)
        print "EXIT STATUS ORIGINAL " + str(self.exitStatus) + " NEW " + str(0)
        self.exitStatus=1
        return self.exitStatus



def sample(self, name, writeOut, writeErr, status, err):
    self.name       = name
    self.exitStatus = 255 #not run
    self.status     = status
    self.err        = err
    self.writeOut   = writeOut
    self.writeErr   = writeErr

    print "RUNNING SAMPLE FUNCTION NAMED " + self.name
    self.status = joblaunch.FINISH
    print "GOT STATUS " + str(status) + " RETURNIN STATUS " + str(self.status)
    print "EXIT STATUS ORIGINAL " + str(self.exitStatus) + " NEW " + str(0)
    self.exitStatus=1
    return self.exitStatus

#sample = sampleWrapper("watever0")

    
