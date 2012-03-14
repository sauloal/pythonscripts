#!/usr/bin/python


def runString(id, cmdFinal, messaging):
    try:
        print "JOB :: " + id + " :: OPENING PROCESS FOR CMD '" + cmdFinal + "'"
        p = subprocess.Popen(cmdFinal, shell = True, executable="/bin/bash", stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT)

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
                print "JOB :: " + id + " :: CMD ARR {" + str(cmd) + "} STR {" + cmdFinal + "} :: RETURNED: " + str(messaging.exitCode) + " THEREFORE FAILED "
                messaging.status = FAILED
                messaging.addError("FAILED TO RUN " + cmdFinal + " :: RETURNED: " + str(messaging.exitCode) + " THEREFORE FAILED ")
                return messaging.exitCode
            #print "FINISHED"

            #print "FINISHED RUNNING CMD " + cmdFinal + " WRITING"
            #Job.outputFileWriter.write(id, p.stdout)
            #print "FINISHED RUNNING CMD " + cmdFinal + " WROTE"
            print "JOB :: " + id + " :: REACHED END. FINISHING WITH STATUS " + STATUSES[messaging.status] + " " + str(messaging.exitCode)
            messaging.status   = FINISH
            messaging.exitCode = 0
            return messaging.exitCode

        except Exception, e:
            print "Exception (Job__launch_out): ", e
            messaging.status = FAILED
            messaging.addError("FAILED TO RUN " + cmdFinal + " EXCEPTION " + str(e))
            messaging.exitCode = 252
            return messaging.exitCode

    except Exception, e:
        print "Exception (Job__launch): ", e
        messaging.status = FAILED
        messaging.addError("FAILED TO RUN " + cmdFinal + " EXCEPTION " + str(e))
        messaging.exitCode = 253
        return messaging.exitCode

