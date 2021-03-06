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
from tools import constants

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
    def __init__(self, name, **kwargs):
        #print "INITING SAMPLE WRAPPER " + name
        self.name     = name
        self.exitCode = 255 #not run
        
        cmd = kwargs.get('cmd', None)
        if cmd is not None:
            self.cmd      = cmd

    def __call__(self, messaging):
        #print "using wrong call"
        self.messaging = messaging

        print "RUNNING WRAPPER NAMED " + self.name
        #print "GOT STATUS " + str(messaging.status)


        initChild = getattr(self, 'initChild', None)
        if initChild is not None:
            #print "HAS INIT CHILD"
            self.initChild()
        else:
            #print "DOESN'T HAVE INIT CHILD"
            pass


        cmd = getattr(self, "parameter", None)
        if cmd is not None:
            run.runString(self.name, self.parameter.getCmd(), messaging)
        else:
            cmd = getattr(self, "cmd", None)
            if cmd is not None:
                run.runString(self.name, cmd, messaging)
            else:
                print "error. no command to run"
                self.messaging.status = constants.FAILED
                print "RETURNING STATUS "     + str(self.messaging.status)
                print "EXIT STATUS ORIGINAL " + str(self.messaging.exitCode)
                self.messaging.exitCode = 256
                print "EXIT STATUS NEW "      + str(self.messaging.exitCode)


        if self.messaging.exitCode != 0:
            print "RETURNING STATUS "     + str(self.messaging.status)
            print "EXIT CODE        "     + str(self.messaging.exitCode)
            print "ERROR            "     + self.messaging.getError()

    def selfTest(self, messaging):
        #messaging.addError("SAMPLE WRAPPER")
        #messaging.addError("  SAMPLE SELF TEST")
        #messaging.addError("    " + str(self))
        #messaging.stdout(self.name, "SAMPLE WRAPPER\n")
        #messaging.stderr(self.name, "  SELF TESTING\n")
        #messaging.stdout(self.name, str(self) + "\n")
        #messaging.status = constants.FINISH
        pass

    def getInputs(self):
        inputs = getattr(self, 'inputs', None)
        return inputs

    def getOutputs(self):
        outputs = getattr(self, 'outputs', None)
        return outputs



def sample(messaging):
    name       = "SaMpLeFuNcTiOn"

    messaging.stdout(name, "RUNNING SAMPLE FUNCTION NAMED " + name + "\n")

    messaging.stdout(name, "GOT STATUS " + str(messaging.status) + "\n")
    messaging.status = constants.FINISH
    messaging.stdout(name, "RETURNING STATUS " + str(messaging.status) + "\n")


    messaging.stdout(name, "EXIT STATUS ORIGINAL " + str(messaging.exitCode) + "\n")
    messaging.exitCode = 255 #not run
    messaging.exitCode = 0
    messaging.stdout(name, "EXIT STATUS NEW " + str(messaging.exitCode) + "\n")


#sample = sampleWrapper("watever0")
