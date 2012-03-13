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



class sampleWrapper():
    def __init__(self, name):
        self.name       = name
        self.exitStatus = 255 #not run

    def __call__(self, writeOut, writeErr, status, err):
        self.status     = status
        self.err        = err
        self.writeOut   = writeOut
        self.writeErr   = writeErr

        print "RUNNING WRAPPER NAMED " + self.name
        self.status = joblaunch.FINISH
        print "GOT STATUS " + str(status) + " RETURNING STATUS " + str(self.status)
        print "EXIT STATUS ORIGINAL " + str(self.exitStatus) + " NEW " + str(0)
        self.exitStatus = 0
        return (self.exitStatus, self.status)
        
    def selfTest(self):
        print "SAMPLE WRAPPER"
        print "  SELF TESTING: "
        print self
        return joblaunch.FINISH



def sample(writeOut, writeErr, status, err):
    exitStatus = 255 #not run
    name       = "SaMpLeFuNcTiOn"

    print "RUNNING SAMPLE FUNCTION NAMED " + name
    status = joblaunch.FINISH
    print "GOT STATUS " + str(status) + " RETURNIN STATUS " + str(status)
    print "EXIT STATUS ORIGINAL " + str(exitStatus) + " NEW " + str(0)
    exitStatus=1
    return (exitStatus, status)

#sample = sampleWrapper("watever0")

    
