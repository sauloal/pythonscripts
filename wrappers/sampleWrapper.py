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
        self.name     = name
        self.exitCode = 255 #not run

    def __call__(self, messaging):
        self.messaging = messaging

        print "RUNNING WRAPPER NAMED " + self.name
        print "GOT STATUS " + str(self.messaging.status)
        self.messaging.status = joblaunch.FINISH
        print "RETURNING STATUS " + str(self.messaging.status)
        print "EXIT STATUS ORIGINAL " + str(self.messaging.exitCode)
        self.messaging.exitCode = 0
        print "EXIT STATUS NEW " + str(self.messaging.exitCode)
        
    def selfTest(self, messaging):
        print "SAMPLE WRAPPER"
        print "  SELF TESTING: "
        print self
        messaging.status = joblaunch.FINISH



def sample(messaging):
    name       = "SaMpLeFuNcTiOn"

    print "RUNNING SAMPLE FUNCTION NAMED " + name

    print "GOT STATUS " + str(messaging.status)
    messaging.status = joblaunch.FINISH
    print "RETURNING STATUS " + str(messaging.status)

    
    print "EXIT STATUS ORIGINAL " + str(messaging.exitCode)
    messaging.exitCode = 255 #not run
    messaging.exitCode = 0
    print "EXIT STATUS NEW " + str(messaging.exitCode)


#sample = sampleWrapper("watever0")

    
