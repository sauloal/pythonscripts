#!/usr/bin/python
import subprocess
import constants
from threading  import Thread
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
        p = subprocess.Popen(cmdFinal, shell = True,
            executable="/bin/bash",
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)

        #http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
        print "JOB :: " + id + " :: OPENING QUEUE OUT"
        q_out = Queue()
        t_out = Thread(target=enqueue_pipe, args=(p.stdout, q_out))
        t_out.daemon = True # thread dies with the program
        t_out.start()

        print "JOB :: " + id + " :: OPENING QUEUE ERR"
        q_err = Queue()
        t_err = Thread(target=enqueue_pipe, args=(p.stderr, q_err))
        t_err.daemon = True # thread dies with the program
        t_err.start()

        try:

            print "JOB :: " + id + " :: CHECKING POOL"
            while not p.poll():
                print "JOB :: " + id + " :: TRYING TO READ PIPE"
                try:
                    lineOut = q_out.get_nowait() # or q.get(timeout=.1)
                except Empty:
                    pass
                    #print('no stderr output yet')
                else: # got line
                    messaging.stdout(id, lineOut, internal=True)

                try:
                    lineErr = q_err.get_nowait() # or q.get(timeout=.1)
                except Empty:
                    pass
                    #print('no stderr output yet')
                else: # got line
                    messaging.stderr(id, lineErr, internal=True)

            print "JOB :: " + id + " :: GETTING RETURN CODE"
            returnCode = p.returncode

            print "JOB :: " + id + " :: WAITING"
            #print "WAITING"
            messaging.exitCode = returnCode
            p.wait()
            if messaging.exitCode:
                print "JOB :: " + id + " :: STR {" + cmdFinal + "} :: RETURNED: " + str(messaging.exitCode) + " THEREFORE FAILED "
                messaging.status = constants.FAILED
                messaging.addError("FAILED TO RUN " + cmdFinal + " :: RETURNED: " + str(messaging.exitCode) + " THEREFORE FAILED ")
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
            messaging.exitCode = 252
            return messaging.exitCode

    except Exception, e:
        print "Exception (Job__launch): ", e
        messaging.status = constants.FAILED
        messaging.addError("FAILED TO RUN " + cmdFinal + " EXCEPTION " + str(e))
        print "FAILED TO RUN " + cmdFinal + " EXCEPTION " + str(e)
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
