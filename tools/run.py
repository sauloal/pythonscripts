def run(**kwargs)
    cmd      = kwargs.get('cmd', None)
    stdinCmd = kwargs.get('stdin', None)

    if not cmd:
        return None

    #TODO: CHECK IF INSTANCE OF LIST, THEN ITERATE
    # OR ITERATOR OR PIPE
    try:
        if stdin:
            p = subprocess.Popen( cmd,
                              stdin  = subprocess.PIPE,
                              stdout = subprocess.PIPE,
                              stderr = subprocess.PIPE,
                              close_fds = True)
            stdout_text, stderr_text = p.communicate(stdinCmd)
        else:
            p = subprocess.Popen( cmd,
                              stdout    = subprocess.PIPE,
                              stderr    = subprocess.PIPE,
                              close_fds = True)
            stdout_text, stderr_text = p.communicate()

        return stdout_text.rstrip()
    except Exception as (e, err):
        print type(inst)     # the exception instance
        print inst.args      # arguments stored in .args
        print inst           # __str__ allows args to printed directly





        # IMPORTANT: In UNIX, Popen uses /bin/sh, whatever the user shell is
        for cmd in self.commands:
            cmdFinal = ""

            if   isinstance(cmd, types.FunctionType):
                self.ret = cmd(Job.outputFileWriter.writelnOut, Job.outputFileWriter.writelnErr, self.status, self.error)
                return
            elif isinstance(cmd, types.InstanceType):
                self.ret = cmd(Job.outputFileWriter.writelnOut, Job.outputFileWriter.writelnErr, self.status, self.error)
                return
            elif isinstance(cmd, types.MethodType):
                self.ret = cmd(Job.outputFileWriter.writelnOut, Job.outputFileWriter.writelnErr, self.status, self.error)
                return
            elif isinstance(cmd, types.ListType):
                for part in cmd:
                    #print "  PART  '" + str(part) + "'"

                    if isinstance(part, types.FunctionType):
                        #print "    FUNCTION"
                        if cmdFinal:
                            cmdFinal += " "
                        cmdFinal += part()
                    elif isinstance(part, types.MethodType):
                        #print "    FUNCTION"
                        if cmdFinal:
                            cmdFinal += " "
                        cmdFinal += part()
                    else:
                        #print "    TEXT"
                        if cmdFinal:
                            cmdFinal += " "
                        cmdFinal += part
                #print "  CMD F '" + str(cmdFinal) + "'"

                try:
                    print "OPENING PROCESS FOR CMD '" + cmdFinal + "'"
                    p = subprocess.Popen(cmdFinal, shell = True, executable="/bin/bash", stdout = subprocess.PIPE,
                        stderr = subprocess.STDOUT)

                    try:
                        (stdOut, stdErr) = p.communicate(input=None)


                        if stdOut:
                            #sys.stdout.write("LINE<1> "+str(stdOut))
                            Job.outputFileWriter.writelnOut(self.id, str(stdOut))

                        if stdErr:
                            #sys.stderr.write("LINE<2> "+str(stdErr))
                            Job.outputFileWriter.writelnErr(self.id, str(stdErr))

                        #print "WAITING"
                        self.ret = p.wait()
                        if self.ret:
                            return
                        #print "FINISHED"

                        #print "FINISHED RUNNING CMD " + cmdFinal + " WRITING"
                        #Job.outputFileWriter.write(self.id, p.stdout)
                        #print "FINISHED RUNNING CMD " + cmdFinal + " WROTE"

                    except Exception, e:
                        print "Exception (Job__launch_out): ", e
                        self.status = FAILED
                        self.error  = "FAILED TO RUN " + cmdFinal + " EXCEPTION " + str(e)
                        self.ret    = 252
                        return

                except Exception, e:
                    print "Exception (Job__launch): ", e
                    self.status = FAILED
                    self.error  = "FAILED TO RUN " + cmdFinal + " EXCEPTION " + str(e)
                    self.ret    = 253
                    return

                if self.ret:
                    self.status = FAILED
                    self.error  = "FAILED TO RUN " + cmdFinal
                    return
            #print " REACHED END. FINISHING WITH STATUS " + str(self.status)
            self.status = FINISH
            self.ret = 0

