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
    the class/function has to accept a messaging class which contains:
        stdout   [function to print to stdout]
        stderr   [function to print to stderr]
        addError [function to add error messages]
        status   [variable containing current running status]
        exitCode [variable containing current exit code]

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
        messaging.addError("SAMPLE WRAPPER")
        messaging.addError("  SAMPLE SELF TEST")
        messaging.addError("    " + str(self))
        messaging.stdout(self.name, "SAMPLE WRAPPER\n")
        messaging.stderr(self.name, "  SELF TESTING\n")
        messaging.stdout(self.name, str(self) + "\n")
        messaging.status = joblaunch.FINISH



def sample(messaging):
    name       = "SaMpLeFuNcTiOn"

    messaging.stdout(name, "RUNNING SAMPLE FUNCTION NAMED " + name + "\n")

    messaging.stdout(name, "GOT STATUS " + str(messaging.status) + "\n")
    messaging.status = joblaunch.FINISH
    messaging.stdout(name, "RETURNING STATUS " + str(messaging.status) + "\n")

    
    messaging.stdout(name, "EXIT STATUS ORIGINAL " + str(messaging.exitCode) + "\n")
    messaging.exitCode = 255 #not run
    messaging.exitCode = 0
    messaging.stdout(name, "EXIT STATUS NEW " + str(messaging.exitCode) + "\n")


#sample = sampleWrapper("watever0")

    
