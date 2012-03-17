#!/usr/bin/python
__version__ = "0.11.01"
__autor__   = "Yassin Ezbakhe <yassin@ezbakhe.es> | Saulo Aflitos <sauloal@gmail.com>"
"""
    Based in the works of Yassin Ezbakhe ( http://code.google.com/p/joblaunch/ )
    and extrapolated to be used as a module. It now has extended capabilities
    such as:
        - stopping branched which have failed to run
        - graphical output of the result
        - standard status nomenclature
        - allows to run classes, functions or strings
        - priority is still the order of the parameters but now it can be
            obtained automatically
        - the number of threads is now limited to the number of requests if
            there are not enough requests

    To initialize the mainLib function takes a list of jobs and parameters (
        the same from command line ).
    Each job should be initialized as such:
                        NAME  LIST OF classes/function/strings  PARAMETERS
    f0 = joblaunch.Job('f0', [sw                      ],        selfTester=sw )
    f1 = joblaunch.Job('f1', [sampleWrapper.sample    ],        deps=[f0] )
    f2 = joblaunch.Job('f2', [['sleep  3;', 'echo f2']],        deps=[f0] )

    classes have to be callable:
        compulsory:
            def __call__(self, messaging)
                where messaging contains:
                    stdout   = function prints to stdout
                    stderr   = function prints to stderr
                    status   = contains the current status of the process
                    exitCode = contains the current error message
                    error    = LIST containing all taceback of errors
                status and err should be returned
        optionally:
            def selfTest(self)
    functions mush receive the same parameters:
        def sample(writeOut, writeErr, status, err)
    strings
"""



import sys
import os
import time
import optparse
import logging
import threading
import multiprocessing
import collections
import Queue
import traceback
import types
import signal
import sys

from run   import runString
import constants

try:
    import pydot
    usePydot = True
except ImportError:
    usePydot = False

try:
    import yaml
    from yaml import load, dump
    useYaml = True

    try:
        from yaml import CLoader as Loader, CDumper as Dumper
        print "USING YAML C VERSION"
    except ImportError:
        from yaml import Loader, Dumper
        print "USING YAML PYTHON VERSION"
except ImportError:
    useYaml = False



debug           = True
global_priority = 0
alwaysDump      = True




#http://stackoverflow.com/questions/4205317/capture-keyboardinterrupt-in-python-without-try-except
def signal_handler(signal, frame):
    print '!'*50
    print "You've sent signal " + str(signal) + ". exiting"
    print '!'*50

    sys.exit(signal)

signal.signal(signal.SIGINT, signal_handler)
logPath = 'joblaunch/' + constants.timestamp
os.mkdir(logPath)



class programMessaging():
    """
    Helper function to transfer between process and subprocesses all information
    needed to report execution status. As it can be passed as reference, any sub-
    process can update the parents result without the need to return anything
    """
    def __init__(self, id, status, exitCode):
        """
        Initialized the id (which will be printed before any message)
        the satus (defined in the header), and the exit code. Create a empty
        error messages list
        """
        self.id          = id
        self.status      = status
        self.exitCode    = exitCode
        self.error       = []

    def setFileWriter(self, fileWriter):
        """
        sets a filewriter and creates a job writer which prepends each message
        with the parent id
        """
        self.fileWritter = fileWriter
        self.jobWritter  = OutputJobWriter(self.id, fileWriter)

    def addError(self, message):
        """
        append de error array with a message prepended with the id
        """
        self.error.append(self.id + " :: " + message)

    def getError(self):
        """
        get the error string
        """
        return "\n".join(self.error)

    def stdout(self, id, message, **kwargs):
        """
        prints a message to stdout prepending with the parent id and the caller id
        """
        self.jobWritter.writelnOut(id, message, **kwargs)

    def stderr(self, id, message, **kwargs):
        """
        prints a message to stderr prepending with the parent id and the caller id
        """
        self.jobWritter.writelnErr(id, message, **kwargs)

def getPriority():
    """
    counter to give priorities to the jobs in the order they are created
    """
    global global_priority
    global_priority       += 1
    return global_priority - 1

class Graph:
    """
    Directed graph class

    We have our own implementation because we don't need all the functionality
    offered by other packages, such as NetworkX.
    """

    (WHITE, GREY, BLACK) = (0, 1, 2)

    def __init__(self):
        """
        Initialize an empty graph.
        """
        self.nodes    = set()
        self.numNodes = 0
        self.edges    = { }

    def addNode(self, node):
        """
        Add a node to the graph. If the node already exists, do nothing.
        """
        if not node in self.nodes:
            self.nodes.add(node)
            self.numNodes   += 1
            self.edges[node] = set()

    def addEdge(self, u, v):
        """
        Add an egde between two nodes in the graph. The nodes are created if
        they don't exist.
        """
        self.addNode(u)
        self.addNode(v)
        self.edges[u].add(v)

    def containsCycle(self):
        """
        Return True if the graph contains a cycle. In our case, a task graph
        that has a cycle with lead to a deadlock.
        """
        # http://www.eecs.berkeley.edu/~kamil/teaching/sp03/041403.pdf
        # In order to detect cycles, we use a modified depth first search
        # called a colored DFS. All nodes are initially marked WHITE. When a
        # node is encountered, it is marked GREY, and when its descendants
        # are completely visited, it is marked BLACK. If a GREY node is ever
        # encountered, then there is a cycle.
        marks = dict([(v, Graph.WHITE) for v in self.nodes])
        def visit(v):
            marks[v] = Graph.GREY
            for u in self.edges[v]:
                if marks[u] == Graph.GREY:
                    return True
                elif marks[u] == Graph.WHITE:
                    if visit(u):
                        return True
            marks[v] = Graph.BLACK
            return False
        for v in self.nodes:
            if marks[v] == Graph.WHITE:
                if visit(v):
                    return True
        return False

    def __iter__(self):
        for u in sorted(self.nodes):
            for v in sorted(self.edges[u]):
                yield (u, v)

    def pringGraph(self):
        pass

class AtomicCounter:
    """
    Counter that implements atomic operations to be used in multiple threads.
    For now, the only operation we need is decrement.
    """

    def __init__(self, value):
        self.value = value
        self.lock  = threading.Lock()

    def decrement(self):
        """
        Decrement the counter and return True if the decremented value is >= 0
        """
        with self.lock:
            res = self.value > 0
            self.value -= 1
        return res

    def quit(self):
        with self.lock:
            res = self.value > 0
            self.value = 0
        return res

    def __repr__(self):
        return str(self.value)

class PriorityQueue(Queue.PriorityQueue):
    """
    Priority queue. The priority is the property 'priority' of the item
    """

    def put(self, item):
        Queue.PriorityQueue.put(self, (item.priority, item))

    def get(self):
        (priority, item) = Queue.PriorityQueue.get(self)
        return item

class OutputFileWriter:
    """
    This clases manages the file where the output of each job is written.
    """

    lock = threading.Lock()

    def __init__(self, outputFilePath, verbose):
        fout = open(outputFilePath, "w") if outputFilePath != "-" else sys.stdout
        self.outputFile = fout
        self.verbose    = verbose

    def write(self, jobId, stdout):
        """
            Write the standard output of a job to the file.
            If self.verbose is True, the job id is also printed and the
            output is tabbed to the right.
        """

        if self.verbose:
            # this is very inefficient if there are too much lines to write
            #output = [ "RUNNING %s\n" % jobId ]
            output = []
            # tab each line two spaces to the right
            output.extend("  " + jobId + ": " + line for line in stdout.readlines())
            #output.append("\n")
        else:
            output = stdout.readlines()

        with OutputFileWriter.lock:
            self.outputFile.writelines(output)

    def writeln(self, jobId, stream, line):
        """
        Automatically prepend the message with jobid and stream
        """
        if self.verbose:
            # this is very inefficient if there are too much lines to write
            #output = [ "RUNNING %s\n" % jobId ]
            output = []
            # tab each line two spaces to the right
            output.append("  " + jobId + stream + ": " + line)
        else:
            output = jobId + ": " + line

        with OutputFileWriter.lock:
            self.outputFile.writelines(output)

    def writelnOut(self, jobId, line):
        """
        Automatically prepend with the jobid and the stream out
        """
        self.writeln(jobId, "<1>", line)

    def writelnErr(self, jobId, line):
        """
        Automatically prepend with the jobid and the stream err
        """
        self.writeln(jobId, "<2>", line)

    def close(self):
        self.outputFile.close()

class OutputJobWriter():
    """
    Wrapper to OutputFileWriter which stores the jobid and prepends it to the
    job id of the caller (think subprocess) unless the named parameter "internal"
    is passed
    """
    def __init__(self, className, writer):
        self.className = className
        self.writer    = writer
        #Job.outputFileWriter     = OutputFileWriter(options.outputFile, options.verbose)
        #OutputFileWriter(outputFile, verbose)
        self.writerOut = OutputFileWriter(logPath + "/jobLaunch_"+className+".out", True)
        self.writerErr = OutputFileWriter(logPath + "/jobLaunch_"+className+".out", True)
        #idStr = constants.getTimestampHighRes()
        #fileName = logPath + '/' + idStr + '.png'

    def write(self, jobId, stdout, **kwargs):
        internal = kwargs.get('internal', None)
        if internal:
            self.writer.write(   jobId, stdout)
            self.writerOut.write(jobId, stdout)
        else:
            self.writer.write(   self.className + " :: " + jobId, stdout)
            self.writerOut.write(self.className + " :: " + jobId, stdout)

    def writeln(self, jobId, stream, line, **kwargs):
        internal = kwargs.get('internal', None)
        if internal:
            self.writer.writeln(   jobId, stream, line)
            self.writerOut.writeln(jobId, stream, line)
        else:
            self.writer.writeln(   self.className + " :: " + jobId, stream, line)
            self.writerOut.writeln(self.className + " :: " + jobId, stream, line)

    def writelnOut(self, jobId, line, **kwargs):
        internal = kwargs.get('internal', None)
        if internal:
            self.writer.writelnOut(   jobId, line)
            self.writerOut.writelnOut(jobId, line)
        else:
            self.writer.writelnOut(   self.className + "<1> :: " + jobId, line)
            self.writerOut.writelnOut(self.className + "<1> :: " + jobId, line)

    def writelnErr(self, jobId, line, **kwargs):
        internal = kwargs.get('internal', None)
        if internal:
            self.writer.writelnErr(   jobId, line)
            self.writerErr.writelnErr(jobId, line)
        else:
            self.writer.writelnErr(   self.className + "<2> :: " + jobId, line)
            self.writerErr.writelnErr(self.className + "<2> :: " + jobId, line)

    def close(self):
        self.writerErr.close()
        self.writerOut.close()


class Job:
    """
    Class that encapsulates a job. Each job consists of an id, a priority
    and a list of commands. This class is responsible of launching
    each of the commands and writing the output and the log to a file.
    exit codes:
        -1 not run
        256 not launched
    """

    outputFileWriter = OutputFileWriter

    def __init__(self, id_, commandsList, **kwargs):
        self.id           = id_
        self.commands     = commandsList
        assert len(self.commands) > 0
        self.predecessors = set()
        self.successors   = set()
        self.messaging    = programMessaging(self.id, constants.NOT_RUN, -1)
        self.selfTester   = kwargs.get('selfTester', self)
        self.priority     = kwargs.get('priority',   getPriority())
        self.deps         = kwargs.get('deps',       [])


    def __call__(self):
        assert not self.predecessors
        logging.info("%s started %s", self.id, threading.currentThread().name)
        begin                   = time.time()

        self.messaging.setFileWriter(Job.outputFileWriter)

        self.messaging.exitCode = 256
        self.messaging.status   = constants.RUNNING
        res                     = self.__launch()
        end                     = time.time()
        logging.info("%s finished %f", self.id, end - begin)
        if self.messaging.status == constants.FINISH:
            if self.selfTester:
                self.selfTester.selfTest(self.messaging)
        self.messaging.jobWritter.close()

        if useYaml and (res or alwaysDump):
            pass

        return res

    def selfTest(self, messaging):
        #print "  LOCAL SELF TESTER"
        pass

    def getStatus(self):
        return self.messaging.status

    def getReturn(self):
        return self.messaging.exitCode

    def getError(self):
        return self.messaging.getError()

    def getCommands(self):
        return self.commands

    def getPredecessors(self):
        return self.predecessors

    def getSuccessors(self):
        return self.successors

    def getDeps(self):
        return self.deps

    def getId(self):
        return self.id

    def __repr__(self):
        return "Job %s" % self.id

    def __launch(self):
        #print "JOB :: " + self.id + " :: COMMANDS " + str(self.commands) + " (" + str(len(self.commands))+ ")"
        # IMPORTANT: In UNIX, Popen uses /bin/sh, whatever the user shell is

        for cmd in self.commands:
            #print "JOB :: " + self.id + " :: CMD " + str(cmd)
            if   isinstance(cmd, types.FunctionType):
                print "JOB :: " + self.id + " :: CMD " + str(cmd) + " :: IS FUNCTION"
                cmd(self.messaging)
                if self.messaging.exitCode:
                    print "JOB :: " + self.id + " :: CMD " + str(cmd) + " :: RETURNED: " + str(self.messaging.exitCode) + " THEREFORE FAILED "
                    self.messaging.status = constants.FAILED
                    self.messaging.addError("FAILED TO RUN FUNCTION " + str(cmd))
                    return self.messaging.exitCode
            elif isinstance(cmd, types.InstanceType):
                print "JOB :: " + self.id + " :: CMD " + str(cmd) + " :: IS INSTANCE"
                cmd(self.messaging)
                if self.messaging.exitCode:
                    print "JOB :: " + self.id + " :: CMD " + str(cmd) + " :: RETURNED: " + str(self.ret) + " THEREFORE FAILED "
                    self.messaging.status = constants.FAILED
                    self.messaging.addError("FAILED TO RUN INSTANCE " + str(cmd))
                    return self.messaging.exitCode
            elif isinstance(cmd, types.MethodType):
                print "JOB :: " + self.id + " :: CMD " + str(cmd) + " :: IS METHOD"
                cmd(self.messaging)
                if self.messaging.exitCode:
                    self.messaging.status = constants.FAILED
                    self.messaging.addError("FAILED TO RUN METHOD " + str(cmd))
                    return self.messaging.exitCode
            elif isinstance(cmd, types.ListType):
                cmdFinal = ""
                #print "JOB :: " + self.id + " :: CMD " + str(cmd) + " :: IS LIST"

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
                    runString(self.id, cmdFinal, self.messaging)
                    return self.messaging.exitCode
                except Exception, e:
                    print "Exception (Job__launch): ", e
                    self.messaging.status = constants.FAILED
                    self.messaging.addError("FAILED TO RUN " + cmdFinal + " EXCEPTION " + str(e))
                    self.messaging.exitCode = 253
                    return self.messaging.exitCode

                if self.messaging.exitCode:
                    self.messaging.status = constants.FAILED
                    self.messaging.addError("FAILED TO RUN " + cmdFinal)
                    self.messaging.exitCode = 251
                    return self.messaging.exitCode

            else:
                print "JOB :: " + self.id + " :: CMD " + str(cmd) + " :: IS UNKOWN TYPE"
                self.messaging.status = constants.FAILED
                self.messaging.addError("NOTHING TO RUN " + str(cmd))
                return self.messaging.exitCode

        print "JOB :: " + self.id + " :: REACHED END. FINISHING WITH STATUS " + constants.STATUSES[self.messaging.status] + " " + str(self.messaging.exitCode)
        self.messaging.status   = constants.FINISH
        self.messaging.exitCode = 0
        return self.messaging.exitCode

class Core(threading.Thread):
    """
    Each object of this class is a thread that schedules jobs to be
    scheduled when they are ready.
    """

    def __init__(self, queue, numJobsLeft):
        super(Core, self).__init__()
        self.queue       = queue
        self.numJobsLeft = numJobsLeft

    def run(self):
        """
        Run in a thread while there are POSSIBLE jobs left
        """

        while self.queue.qsize():
            job = self.queue.get()
            self.last = job

            job()
            job.printer.printGraph(None, job.getId())

            if not job.getReturn():
                self.__addPreparedJobsToQueue(job)
                self.numJobsLeft.decrement()
            else:
                print job.getError()

    def __addPreparedJobsToQueue(self, job):
        """
        When a job has finished its execution, this method is called so as
        to put in the queue the jobs that were waiting for it (sucessors) and
        are not waiting for any other job.
        """

        if job.getStatus() == constants.FINISH:
            for succ in job.successors:
                succ.predecessors.remove(job)
                if not succ.predecessors:
                    self.queue.put(succ)
                else:
                    pass
        else:
            pass

def check(condition, errorMsg):
    """
    Simple error handler. If the condition is False, write the error to
    console and abort program execution.
    """
    if not condition:
        if debug:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
        sys.stderr.write("%s: error: %s\n" % (sys.argv[0], errorMsg))
        sys.exit(1)

def parseInput(inputFilePath):
    """
    Open the input file, parse it and return the dependency graph,
    the dictionary with the commands lists and the dictionary with the ids
    for each job.

    Input file must have the following format:

    <number of jobs>
    <command>*
    <dependency>*

    where:

        - <number of jobs> is a positive integer to indicate the number of jobs
          to run.
        - <command> is a job name followed by a command. The name can be any
          combination of numbers, letters and punctuation marks (no spaces).
          The command is executed as is through the shell (it can have
          redirections, pipes, expansions, multiple expressions, ...).
        - <dependency> is a list of job names (JA, JB1, ..., JBn) separated by
          spaces. It indicates that job JA depends on jobs JB1, ..., JBn
          (that is, JA can't be executed until all JBx have finished).
    """

    def parseDependencies(text):
        """
        Parse the dependencies part and return a dependency graph, where there
        is an edge between nodes JB and JA if JA depends on JB.
        """
        G = Graph()
        for line in text:
            # tokens = [ JA, JB1, ..., JBn ]
            tokens = line.strip().split()
            check(len(tokens) >= 2, "input file has an invalid syntax")
            JA = tokens[0]
            for JB in tokens[1:]:
                G.addEdge(JB, JA)
        return G

    def parseCommands(text):
        """
        Parse the commands part and return a dictionary, where entry J
        is a list with the commands for job J.
        """
        commands = collections.defaultdict(list)
        for line in text:
            (job, cmd) = line.strip().split(None, 1)
            commands[job].append([cmd])
        return commands

    def getJobsOrder(text):
        """
        Return ids for jobs (the ordering is the same as the used in the input
        file) and return a dictionary where entry J is the id of job J.
        """
        jobsOrder = { }
        id_ = 0
        for line in text:
            (job, _) = line.strip().split(None, 1)
            if job not in jobsOrder:
                jobsOrder[job] = id_
                id_ += 1
        return jobsOrder

    def getChecks(commands):
        checks = {}
        for job in commands:
            checks[job] = checkOut
        return checks

    # open and read input file
    try:
        f     = open(inputFilePath) if inputFilePath != "-" else sys.stdin
        lines = f.readlines()
        check(len(lines) > 0, "input file is empty")
        f.close()
    except IOError as e:
        check(False, e.strerror)

    # split file
    numJobs          = abs(int(lines[0]))
    commandsText     = lines[1:numJobs + 1]
    dependenciesText = lines[numJobs + 1:]

    # parse file
    commands     = parseCommands(commandsText)
    dependencies = parseDependencies(dependenciesText)
    jobsOrder    = getJobsOrder(commandsText)
    checks       = getChecks(commands)

    return (commands, dependencies, jobsOrder, checks)

class jobsList():
    def __init__(self):
        self.items = {}
        pass

    def __setitem__(self, key, item):
        print "SETTING " + str(key) + " item " + str(item)
        self.items[key] = item

    def __iter__(self):
        return self.items.__iter__()

    def __getitem__(self, key):
        return self.items[key]

    def __len__(self):
        return len(self.items)


def createJobs(commands, G, jobsOrder, checks):
    """
    Create a Job object for each job, filling the successors and predecessors
    lists, and return the jobs dictionary, where the key is the id
    and the value is the Job object.
    """

    def getJob(jobId):
        # create a new job or return the existing one
        if jobId not in jobs:
            jobs[jobId] = Job(jobId, commands[jobId], checks[jobId], priority=jobsOrder[jobId])
        return jobs[jobId]

    jobs           = jobsList()
    jobs.G         = G
    printer        = printG(G, jobs)
    jobs.printer   = printer

    for (u, v) in G:
        uJob = getJob(u)
        vJob = getJob(v)
        uJob.successors.add(vJob)
        vJob.predecessors.add(uJob)


    # add jobs not listed in the dependency list (jobs that don't depend on
    # other jobs nor others depend on them)
    for jobId in commands:
        if jobId not in jobs:
            jobs[jobId] = Job(jobId, commands[jobId], checks[jobId], priority=jobsOrder[jobId])
            jobs[jobId].printer = jobs.printer

    assert len(commands) == len(jobs)

    return jobs

def createQueue(jobs):
    """
    Create and return the initial job queue with jobs that don't depend
    on any other.
    """
    q = PriorityQueue()
    for t in jobs:
        if not jobs[t].predecessors:
            q.put(jobs[t])
    check(not q.empty(), "no initial job found to launch due to dependency cycles")
    return q

def start(jobs, numThreads):
    """
    Launch threads and begin working. The function waits for all jobs to end.
    """

    jobsQueue   = createQueue(jobs)
    numJobsLeft = AtomicCounter(len(jobs))

    cores = [ ]
    maxThreads = numThreads
    if numThreads > len(jobs):
        maxThreads = len(jobs)

    print "START :: CREATING THREADS " + str(maxThreads)
    for i in range(maxThreads):
        core = Core(jobsQueue, numJobsLeft)
        cores.append(core)
        core.start()
        time.sleep(1)
    print "START :: THREADS CREATED"

    print "START :: FINISHED RUNNING. JOINING CORES"
    time.sleep(1)

    while core.numJobsLeft > 0:
        print "START :: WATING JOBS: " + str(core.numJobsLeft)
        time.sleep(1)

    time.sleep(1)
    print "START :: FINISHED RUNNING. JOINING CORES"

    for core in cores:
        core.join()
    print "START ::   FINISHED JOINING "


def getCPUCount():
    """
    Return the number of cores in the machine.
    """
    return multiprocessing.cpu_count()

def parseArguments(args):
    """
    Parse program arguments and return options used by user.
    """

    usage       = "%prog [options] inputFile"
    version     = "%%prog %s" % __version__
    description = ( \
        "%prog is a parallel job scheduler. It is used to schedule jobs in a "
        "multithreads environment, where each job must wait for others to "
        "finish before being launched. Each job consists of one or more "
        "commands. A command can have anything that can be interpreted by the "
        "shell, e.g. pipes, redirections, etc.")
    epilog = "Written by Yassin Ezbakhe <yassin@ezbakhe.es>"

    parser = optparse.OptionParser(usage = usage, version = version,
        description = description, epilog = epilog)

    parser.add_option("-n", "--numThreads",
                      action = "store", type = "int", dest = "numThreads",
                      default = getCPUCount(),
                      help = "maximum number of threads to run concurrently "
                             "[default: %default]")
#    parser.add_option("-i", "--input-file",
#                      action = "store", dest = "inputFile", default = "-",
#                      help = "read jobs from INPUTFILE (if -, read from "
#                             "standard input) [default: %default]")
    parser.add_option("-l", "--log-file",
                      action = "store", dest = "logFile",
                      help = "log all messages to LOGFILE")
    parser.add_option("-o", "--output-file",
                      action = "store", dest = "outputFile", default = "-",
                      help = "redirect all jobs stdout and stderr to OUTPUTFILE "
                             "(if -, redirect to standard output) "
                             "[default: %default]")
    parser.add_option("--force",
                      action = "store_true", dest = "force", default = False,
                      help = "force execution of jobs without checking for "
                             "dependency cycles (MAY CAUSE DEADLOCKS!)")
    parser.add_option("-v", "--verbose",
                      action = "store_true", dest = "verbose", default = False,
                      help = "turn on verbose output")

    (options, args) = parser.parse_args(args)

    # use stdin if no inputFile is given as argument
    options.inputFile = args[0] if len(args) > 0 else "-"

    return options

class printG:
    def __init__(self, G, jobs):
        """
        Prints a png image of the process and the states they are
        TODO:   Allow to change the name
                Allow to append timestamp to create a series of snapshots
        """
        #https://docs.google.com/viewer?url=http://www.graphviz.org/pdf/dotguide.pdf
        #http://pythonhaven.wordpress.com/2009/12/09/generating_graphs_with_pydot/

        self.G        = G
        self.jobs     = jobs

        self.statusColors = {   constants.NOT_RUN: ["white",  "black"],
                                constants.RUNNING: ["yellow", "black"],
                                constants.FAILED:  ["red",    "black"],
                                constants.FINISH:  ["green",  "black"]
                            }

    def printGraph(self, fileName=None, id=None):
        if not usePydot:
            return

        self.graph = pydot.Dot(graph_type='digraph')

        nodes = {}
        for jobId in self.jobs:
            job          = self.jobs[jobId]
            status       = job.getStatus()
            statusColor  = self.statusColors[status]
            node         = pydot.Node(jobId, style="filled", fillcolor=statusColor[0], fontcolor=statusColor[1])
            self.graph.add_node(node)
            nodes[jobId] = node

        for jobId in self.jobs:
            job  = self.jobs[jobId]
            node = nodes[jobId]
            DEPS = job.getDeps()
            #print "ADDING NODE " + jobId + " STATUS: " + str(job.getStatus()) + " RETURN VALUE: " + str(job.getReturn())
            for DEP in DEPS:
                depId   = DEP.getId()
                #print "  DEP " + depId
                depNode = nodes[depId]
                self.graph.add_edge(pydot.Edge(depNode, node))


            #    str = """
            #digraph G {
            #    size ="4,4";
            #    main [shape=box]; /* this is a comment */
            #    main -> parse [weight=8];
            #    parse -> execute;
            #    main -> init [style=dotted];
            #    main -> cleanup;
            #    execute -> { make_string; printf}
            #    init -> make_string;
            #    edge [color=red]; // so is this
            #    main -> printf [style=bold,label="100 times"];
            #    make_string [label="make a\\nstring"];
            #    node [shape=box,style=filled,color=".7 .3 1.0"];
            #    execute -> compare;
            #}
            #"""

            #dot -T svg nato

            #digraph G {
            #subgraph cluster0 {
            #node [style=filled,color=white];
            #style=filled;
            #color=lightgrey;
            #a0 -> a1 -> a2 -> a3;
            #label = "process #1";
            #}
            #subgraph cluster1 {
            #node [style=filled];
            #b0 -> b1 -> b2 -> b3;
            #label = "process #2";
            #color=blue
            #}
            #start -> a0;
            #start -> b0;
            #a1 -> b3;
            #b2 -> a3;
            #a3 -> a0;
            #a3 -> end;
            #b3 -> end;
            #start [shape=Mdiamond];
            #end [shape=Msquare];
            #}

        if fileName is None:
            idStr = constants.getTimestampHighRes()
            if id is not None:
                idStr += '_' + id
            fileName = logPath + '/' + idStr + '.png'

        print "EXPORTING GRAPH PNG " + fileName
        self.graph.write_png(fileName)

def main():
    print "RUNNING MAIN"
    options   = parseArguments(sys.argv[1:])
    inputFile = options.inputFile

    if options.logFile:
        logging.basicConfig(level    = logging.INFO,
                            filename = options.logFile,
                            format   = "%(asctime)s %(message)s",
                            datefmt  = "%Y-%m-%d %H:%M:%S")

    # set output writer
    Job.outputFileWriter     = OutputFileWriter(options.outputFile, options.verbose)

    # parse input file
    (commands, G, jobsOrder, checks) = parseInput(inputFile)

    # check that there are no dependency cycles
    if not options.force:
        check(not G.containsCycle(), "there are dependency cycles (use --force)")

    # check that all jobs have a command
    check(all(job in commands for job in G.nodes), "some jobs don't have a command")

    #create jobs
    jobs        = createJobs(commands, G, jobsOrder, checks)

    jobs.printer.printGraph()

    # begin working
    start(jobs, options.numThreads)

    jobs.printer.printGraph()



###############
# LIBRARY IMPLEMENTATION
###############
def checkGraph(jobs, **kwargs):
    """
    Check if graph contains cycle
    """

    force      = kwargs.get('force')
    G = Graph()

    for jobId in jobs:
        job  = jobs[jobId]
        DEPS = job.getDeps()
        for DEP in DEPS:
            G.addEdge(DEP, job)

    for (uJob, vJob) in G:
        uJob.successors.add(vJob)
        vJob.predecessors.add(uJob)

    # check that there are no dependency cycles
    if not force:
        check(not G.containsCycle(), "there are dependency cycles (use --force)")

    # check that all jobs have a command
    #check(all(job in commands for job in G.nodes), "some jobs don't have a command")
    return G




def mainLib(jobsData, **kwargs):
    """
    takes a list of job classes and run them
    accepts as kwargs:
        verbose    - print job name before each line (unused now)
        force      - execute even if there's cycle in the graph
        numThreads - max number of threads
        outputFile - output file name (default: stdout)
        logFile    - log file name (default: none)
    TODO: explain whole process
    """
    print "RUNNING MAIN LIB"
    verbose    = kwargs.get('verbose',    False)
    force      = kwargs.get('force',      False)
    numThreads = kwargs.get('threads',    getCPUCount())
    outputFile = kwargs.get('outfile',    logPath + "/jobLaunch.out")
    logFile    = kwargs.get('logFile',    logPath + "/jobLaunch.log")

    #TODO: WRITE TO STRING?
    Job.outputFileWriter     = OutputFileWriter(outputFile, verbose)

    if logFile:
        logging.basicConfig(level    = logging.INFO,
                            filename = logFile,
                            format   = "%(asctime)s %(message)s",
                            datefmt  = "%Y-%m-%d %H:%M:%S")

    # parse input file


    jobs            = jobsList()

    for jobId in jobsData.keys():
        job         = jobsData[jobId]
        jobs[jobId] = job

    G               = checkGraph(jobs, force=force)
    jobs.G          = G
    printer         = printG(G, jobs)
    jobs.printer    = printer

    for jobId in jobs:
        job = jobs[jobId]
        job.printer = jobs.printer


    jobs.printer.printGraph()
    # begin working
    start(jobs, numThreads)

    jobs.printer.printGraph()

    return jobs



if __name__ == "__main__":
    if sys.version_info < (2, 6):
        error("Python >= 2.6 is required")

    try:
        if False:
            main()
        else:
            f1 = Job('f1', [['sleep 1; echo f1']] )
            f2 = Job('f2', [['sleep 1; echo f2']] )
            f3 = Job('f3', [['sleep 1; echo f3']] )
            l1 = Job('l1', [['sleep 1; echo l1']], deps=[f1, f2, f3] )
            f4 = Job('f4', [['sleep 1; echo f4']] )
            f5 = Job('f5', [['sleep 1; echo f5']] )
            f6 = Job('f6', [['sleep 1; echo f6']] )
            l2 = Job('l2', [['sleep 1; echo l2']], deps=[f4, f5, f6] )
            d1 = Job('d1', [['sleep 1; echo d1']], deps=[l1, l2] )

            data = {'f1': f1,
                    'f2': f2,
                    'f3': f3,
                    'l1': l1,
                    'f4': f4,
                    'f5': f5,
                    'f6': f6,
                    'l2': l2,
                    'd1': d1}

            mainLib(data)
    except Exception as e:
        print "ERROR RUNNING MAIN"
        check(False, e)
