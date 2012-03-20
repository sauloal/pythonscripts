#!/usr/bin/python
import subprocess
import constants
from threading  import Thread
import sys, traceback
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x


def enqueue_pipe(pipe, queue):
    for line in iter(pipe.readline, b''):
        queue.put(line)
    pipe.close()



def runString(id, cmdFinal, messaging):
    try:
        print "JOB :: " + id + " :: OPENING PROCESS FOR CMD '" + cmdFinal + "'"

        q_out = Queue()
        q_err = Queue()
        
        p = subprocess.Popen(cmdFinal, shell=True,
            executable="/bin/bash",
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)

        #http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python

        t_err = Thread(target=enqueue_pipe, args=(p.stderr, q_err))
        t_err.daemon = True # thread dies with the program
        t_err.start()

        t_out = Thread(target=enqueue_pipe, args=(p.stdout, q_out))
        t_out.daemon = True # thread dies with the program
        t_out.start()



        pid           = p.pid
        messaging.pid = pid

        try:

            print "JOB :: " + id + " :: CHECKING POOL"
            while p.poll() is None:
                #print "JOB :: " + id + " :: TRYING TO READ PIPE (" + str(p.poll()) + ")"
                try:
                    #lineOut = q_out.get_nowait()
                    lineOut = q_out.get(timeout=1)
                    messaging.stdout(id, lineOut, internal=True)
                except Empty:
                    pass
                    #print('no stderr output yet')
                #else: # got line
                    

                try:
                    #lineErr = q_err.get_nowait()
                    lineErr = q_err.get(timeout=1)
                    messaging.stderr(id, lineErr, internal=True)
                except Empty:
                    pass
                    #print('no stderr output yet')
                #else: # got line
                    


            print "JOB :: " + id + " :: GETTING RETURN CODE"
            returnCode = p.returncode

            print "JOB :: " + id + " :: WAITING"
            #print "WAITING"
            messaging.exitCode = returnCode
            p.wait()
            
            while not q_out.empty():
                messaging.stdout(id, q_out.get_nowait(), internal=True)
            while not q_err.empty():
                messaging.stderr(id, q_err.get_nowait(), internal=True)
                
            q_err.join()
            q_out.join()
            t_err.join()
            t_out.join()
            
            if messaging.exitCode:
                print "JOB :: " + id + " :: STR {" + cmdFinal + "} :: RETURNED: " + str(messaging.exitCode) + " THEREFORE FAILED "
                messaging.status = constants.FAILED
                messaging.addError("FAILED TO RUN " + cmdFinal + " :: RETURNED: " + str(messaging.exitCode) + " THEREFORE FAILED ")
                traceback.print_exc()
                return messaging.exitCode
            #print "FINISHED"

            #print "FINISHED RUNNING CMD " + cmdFinal + " WRITING"
            #Job.outputFileWriter.write(id, p.stdout)
            #print "FINISHED RUNNING CMD " + cmdFinal + " WROTE"
            print "JOB :: " + id + " :: REACHED END. FINISHING WITH STATUS " + constants.STATUSES[messaging.status] + " " + str(messaging.exitCode)
            messaging.status   = constants.FINISH
            messaging.exitCode = 0
            return messaging.exitCode

        except Exception, e:
            print "Exception (Job__launch_out): ", e
            messaging.status = constants.FAILED
            messaging.addError("FAILED TO RUN " + cmdFinal + " EXCEPTION " + str(e))
            traceback.print_exc()
            messaging.exitCode = 252
            return messaging.exitCode

    except Exception, e:
        print "Exception (Job__launch): ", e
        messaging.status = constants.FAILED
        messaging.addError("FAILED TO RUN " + cmdFinal + " EXCEPTION " + str(e))
        print "FAILED TO RUN " + cmdFinal + " EXCEPTION " + str(e)
        traceback.print_exc()
        messaging.exitCode = 253
        return messaging.exitCode






#try:
#    (stdOut, stdErr) = p.communicate(input=None)
#
#    try:
#        line = q_out.get_nowait() # or q.get(timeout=.1)
#    except Empty:
#        print('no output yet')
#    else: # got line
#        print line
#
#    if stdOut:
#        #sys.stdout.write("LINE<1> "+str(stdOut))
#        messaging.stdout(id, str(stdOut), internal=True)
#
#    if stdErr:
#        #sys.stderr.write("LINE<2> "+str(stdErr))
#        messaging.stderr(id, str(stdErr), internal=True)
#
#    #print "WAITING"
#    messaging.exitCode = p.wait()
#    if messaging.exitCode:
#        print "JOB :: " + id + " :: STR {" + cmdFinal + "} :: RETURNED: " + str(messaging.exitCode) + " THEREFORE FAILED "
#        messaging.status = constants.FAILED
#        messaging.addError("FAILED TO RUN " + cmdFinal + " :: RETURNED: " + str(messaging.exitCode) + " THEREFORE FAILED ")
#        return messaging.exitCode
#    #print "FINISHED"
#
#    #print "FINISHED RUNNING CMD " + cmdFinal + " WRITING"
#    #Job.outputFileWriter.write(id, p.stdout)
#    #print "FINISHED RUNNING CMD " + cmdFinal + " WROTE"
#    print "JOB :: " + id + " :: REACHED END. FINISHING WITH STATUS " + constants.STATUSES[messaging.status] + " " + str(messaging.exitCode)
#    messaging.status   = constants.FINISH
#    messaging.exitCode = 0
#    return messaging.exitCode
