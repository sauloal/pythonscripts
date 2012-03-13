if __name__ == "__main__":
    import os
    import sys

    fullpath=os.getcwd()

    # add parent folder to path
    
    #print "CURRENT PATH " + fullpath
    fullpath=os.path.abspath(fullpath + "/..")
    #print "PREVIOUS PATH " + fullpath
    sys.path.append(fullpath)
    #print "PATH " + str(sys.path)

from tools import *
"""
    sample class showing how to create a sample program wrapper
    the class/function has to accept:
        writeOut [file handler to print to stdout]
        writeErr [file handler to print to stderr]
        status [ variable containing current running status]
        err [variable containing the current error message]
    and should return:
        status
        err
    status can be found on the header of joblaunch.py
        NOT_RUN         = 0
        RUNNING         = 1
        FAILED          = 2
        FINISH          = 3
    
    Optionally (if used), a class can contain a function called
    "selfTest" which will be called by the end of the execution
    by the job scheduler.
"""


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
    print "GOT STATUS " + str(status) + " RETURNING STATUS " + str(status)
    print "EXIT STATUS ORIGINAL " + str(exitStatus) + " NEW " + str(0)
    exitStatus=0
    return (exitStatus, status)

#sample = sampleWrapper("watever0")

    
