#!/usr/bin/python
import subprocess
import constants
import Queue

def enqueue_pipe(pipe, queue):
    for line in iter(pipe.readline, b''):
        queue.put(line)
    pipe.close()



def runString(id, cmdFinal, messaging):
    try:
        print "JOB :: " + id + " :: OPENING PROCESS FOR CMD '" + cmdFinal + "'"
        p = subprocess.Popen(cmdFinal, shell = True, executable="/bin/bash", stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)

        q_out = Queue()
        t_out = Thread(target=enqueue_pipe, args=(p.stdout, q_out))
        t_out.daemon = True # thread dies with the program
        t_out.start()
        q_err = Queue()
        t_err = Thread(target=enqueue_pipe, args=(p.stderr, q_err))
        t_err.daemon = True # thread dies with the program
        t_err.start()


        try:
            (stdOut, stdErr) = p.communicate(input=None)

            if stdOut:
                #sys.stdout.write("LINE<1> "+str(stdOut))
                messaging.stdout(id, str(stdOut), internal=True)

            if stdErr:
                #sys.stderr.write("LINE<2> "+str(stdErr))
                messaging.stderr(id, str(stdErr), internal=True)

            #print "WAITING"
            messaging.exitCode = p.wait()
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
        messaging.exitCode = 253
        return messaging.exitCode
