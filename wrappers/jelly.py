import os
import sys
import glob
from types import *

if __name__ == "__main__":
    fullpath=os.getcwd()

    # add parent folder to path

    #print "CURRENT PATH " + fullpath
    fullpath=os.path.abspath(fullpath + "/..")
    #print "PREVIOUS PATH " + fullpath
    sys.path.append(fullpath)
    #print "PATH " + str(sys.path)

from tools import *
from tools.parameters import parameters
from tools.parameters import io
from sampleWrapper    import sampleWrapper

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





exe       = "/home/aflit001/bin/jellyfish"
className = 'jelly'




def checkOutput(output):
    pass



class jellyCount(sampleWrapper):
    def __init__(self, **kwargs):
        """
        Usage: jellyfish count [options] file:path+

        Count k-mers or qmers in fasta or fastq files

        Options (default value in (), *required):
         -m, --mer-len=uint32                    *Length of mer
         -s, --size=uint64                       *Hash size
         -t, --threads=uint32                     Number of threads (1)
         -o, --output=string                      Output prefix (mer_counts)
         -c, --counter-len=Length in bits         Length of counting field (7)
             --out-counter-len=Length in bytes    Length of counter field in output (4)
         -C, --both-strands                       Count both strand, canonical representation (false)
         -p, --reprobes=uint32                    Maximum number of reprobes (62)
         -r, --raw                                Write raw database (false)
         -q, --quake                              Quake compatibility mode (false)
             --quality-start=uint32               Starting ASCII for quality values (64)
             --min-quality=uint32                 Minimum quality. A base with lesser quality becomes an N (0)
         -L, --lower-count=uint64                 Don't output k-mer with count < lower-count
         -U, --upper-count=uint64                 Don't output k-mer with count > upper-count
             --matrix=Matrix file                 Hash function binary matrix
             --timing=Timing file                 Print timing information
             --stats=Stats file                   Print stats
             --usage                              Usage
         -h, --help                               This message
             --full-help                          Detailed help
         -V, --version                            Version
        """

        self.input    = kwargs.get("_input", None)
        self.name     = kwargs.get("_name",  None)
        self.force    = kwargs.get("_force", False)
        self.kwargs   = kwargs
        
        assert self.input is not None
        assert self.name  is not None

        function  = "count"
        nickName  = className + "_" + function + "_" + self.name
        print "  INITING JELLY " + function.upper() + " " + nickName
        print "    INPUT " + str(self.input)
        #super(jellyCount, self).__init__(nickName)
        #sampleWrapper.__init__(self, nickName)

        self.function = function
        self.nickName = nickName

    def getInput(self):
        return self.input

    def getOutput(self):
        return io(self.output)

    def __call__(self, messaging):
        #print "using correct call"
        self.initChild()
        if not io(self.outputs).exists():
            print "RUNNING"
            sampleWrapper.__call__(self, messaging)
        else:
            print "SKIPPING"
            #print "error. no command to run"
            messaging.status = constants.SKIPPED
            print "RETURNING STATUS "     + str(messaging.status)
            print "EXIT STATUS ORIGINAL " + str(messaging.exitCode)
            messaging.exitCode = 0
            print "EXIT STATUS NEW "      + str(messaging.exitCode)

    def initChild(self):
        #print "RUNNING RIGHT INIT CHILD"
        input    = self.input
        name     = self.name
        kwargs   = self.kwargs
        function = self.function
        nickName = self.nickName

        output = kwargs.get('output', None)
        if output is None:
            inputBase  = os.path.commonprefix( io(input).getFiles() )
            output     = inputBase + "_mer_counts"
            print "NO OUTPUT GIVEN " + output


        mer_len = kwargs.get('mer_len', None)
        if mer_len is None:
            kwargs['mer_len'] = 31
            print "NO MER LEN " + str(kwargs['mer_len'])


        hashsize = kwargs.get('size', None)
        if hashsize is None:
            kwargs['size']    = 10000000
            print "NO SIZE GIVEN " + str(kwargs['size'])


        parameter = parameters()
        parameter.append(exe,           True,   'name')
        parameter.append(function,      True,   'name')


        params = {
            'mer-len'         : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'size'            : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'threads'         : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'counter-len'     : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'out-counter-len' : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'both-strands'    : { 'type': 'bool'                              },
            'reprobes'        : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'raw'             : { 'type': 'bool'                              },
            'quake'           : { 'type': 'bool'                              },
            'quality-start'   : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'min-quality'     : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'lower-count'     : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'upper-count'     : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'matrix'          : { 'type': 'file', 'dashes': 2, 'equal': True  },
            'timing'          : { 'type': 'file', 'dashes': 2, 'equal': True  },
            'stats'           : { 'type': 'file', 'dashes': 2, 'equal': True  },
        }


        self.input     = io(input)
        self.output    = output

        print "!!!!!!!! INPUT " + str(self.input)
        parameter.parseList(params, kwargs)
        parameter.parse( 'output', 'file',  2,      True,  self.output )
        parameter.parse( '',       'file',  0,      False, self.input  )


        self.parameter = parameter


        self.inputs    = [ self.input        ]
        self.outputs   = [ self.output + '*' ]


        if (parameter.hasParam('matrix')):
            self.inputs.append(io(parameter.getValue('matrix')))
        if (parameter.hasParam('timing')):
            self.outputs.append(io(parameter.getValue('timing')))
        if (parameter.hasParam('stats')):
            self.outputs.append(io(parameter.getValue('stats')))


        print "  INITING JELLY COUNT CMD " + self.parameter.getCmd()
        print "    INPUTS : " + str(self.inputs)
        for inp in self.inputs:
            print str(inp) + "\n"
            
        print "    OUTPUTS: " + str(self.outputs)
        for out in self.outputs:
            print str(out) + "\n"




class jellyStats(sampleWrapper):
    def __init__(self, input=None, _name=None, **kwargs):
        """
        Usage: jellyfish stats [options] db:path

        Statistics

        Display some statistics about the k-mers in the hash:

        Unique:    Number of k-mers which occur only once.
        Distinct:  Number of k-mers, not counting multiplicity.
        Total:     Number of k-mers, including multiplicity.
        Max_count: Maximum number of occurrence of a k-mer.

        Options (default value in (), *required):
         -L, --lower-count=uint64                 Don't consider k-mer with count < lower-count
         -U, --upper-count=uint64                 Don't consider k-mer with count > upper-count
         -v, --verbose                            Verbose (false)
         -o, --output=c_string                    Output file
             --usage                              Usage
         -h, --help                               This message
         --full-help                          Detailed help
        -V, --version                            Version
        """

        assert input  is not None
        assert _name  is not None
        function  = "stats"
        nickName  = className + "_" + function + "_" + _name
        print "  INITING JELLY " + function.upper() + " " + nickName
        sampleWrapper.__init__(self, nickName)
        self.input    = input
        self.function = function
        self.nickName = nickName
        self.name     = _name
        self.kwargs   = kwargs

    def getInput(self):
        return self.input

    def getOutput(self):
        return io(self.output)

    def __call__(self, messaging):
        #print "using correct call"
        self.initChild()
        if not io(self.outputs).exists():
            print "RUNNING"
            sampleWrapper.__call__(self, messaging)
        else:
            print "SKIPPING"
            #print "error. no command to run"
            messaging.status = constants.SKIPPED
            print "RETURNING STATUS "     + str(messaging.status)
            print "EXIT STATUS ORIGINAL " + str(messaging.exitCode)
            messaging.exitCode = 0
            print "EXIT STATUS NEW "      + str(messaging.exitCode)

    def initChild(self):
        #print "RUNNING RIGHT INIT CHILD"
        input    = self.input
        name     = self.name
        kwargs   = self.kwargs
        function = self.function
        nickName = self.nickName


        output = kwargs.get('output', None)
        if output is None:
            output          = input + ".stats"



        parameter = parameters()
        parameter.append(exe,           True,   'name')
        parameter.append(function,      True,   'name')

        params = {
            'lower-count' : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'upper-count' : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'verbose'     : { 'type': 'bool', 'dashes': 2, 'equal': None  }
        }

        parameter.parseList(params, kwargs)
        self.input     = io(input)
        self.output    = output

        parameter.parseList(params, kwargs)
        parameter.parse( 'output', 'file',  2,      True,  self.output )
        parameter.parse( '',       'file',  0,      False, self.input  )


        self.parameter = parameter


        self.inputs    = [ self.input  ]
        self.outputs   = [ self.output ]

        print "  INITING JELLY STATS CMD " + self.parameter.getCmd()
        print "    INPUTS : " + str(self.inputs)
        for inp in self.inputs:
            print str(inp) + "\n"
            
        print "    OUTPUTS: " + str(self.outputs)
        for out in self.outputs:
            print str(out) + "\n"




class jellyHisto(sampleWrapper):
    def __init__(self, input=None, _name=None, **kwargs):
        """
        Usage: jellyfish histo [options] db:path

        Create an histogram of k-mer occurrences

        Create an histogram with the number of k-mers having a given
        count. In bucket 'i' are tallied the k-mers which have a count 'c'
        satisfying 'low+i*inc <= c < low+(i+1)*inc'. Buckets in the output are
        labeled by the low end point (low+i*inc).

        The last bucket in the output behaves as a catchall: it tallies all
        k-mers with a count greater or equal to the low end point of this
        bucket.

        Options (default value in (), *required):
         -l, --low=uint64                         Low count value of histogram (1)
         -h, --high=uint64                        High count value of histogram (10000)
         -i, --increment=uint64                   Increment value for buckets (1)
         -t, --threads=uint32                     Number of threads (1)
         -f, --full                               Full histo. Don't skip count 0. (false)
         -o, --output=c_string                    Output file
         -v, --verbose                            Output information (false)
             --usage                              Usage
             --help                               This message
             --full-help                          Detailed help
         -V, --version                            Version
        """

        assert input  is not None
        assert _name  is not None
        function  = "histo"
        nickName  = className + "_" + function + "_" + _name
        print "  INITING JELLY " + function.upper() + " " + nickName
        sampleWrapper.__init__(self, nickName)
        self.input    = input
        self.function = function
        self.nickName = nickName
        self.name     = _name
        self.kwargs   = kwargs

    def getInput(self):
        return self.input

    def getOutput(self):
        return io(self.output)

    def __call__(self, messaging):
        #print "using correct call"
        self.initChild()
        if not io(self.outputs).exists():
            print "RUNNING"
            sampleWrapper.__call__(self, messaging)
        else:
            print "SKIPPING"
            #print "error. no command to run"
            messaging.status = constants.SKIPPED
            print "RETURNING STATUS "     + str(messaging.status)
            print "EXIT STATUS ORIGINAL " + str(messaging.exitCode)
            messaging.exitCode = 0
            print "EXIT STATUS NEW "      + str(messaging.exitCode)

    def initChild(self):
        #print "RUNNING RIGHT INIT CHILD"
        input    = self.input
        name     = self.name
        kwargs   = self.kwargs
        function = self.function
        nickName = self.nickName



        output = kwargs.get('output', None)
        if output is None:
            output          = input + ".histo"

        parameter = parameters()
        parameter.append(exe,           True,   'name')
        parameter.append(function,      True,   'name')

        params = {
            'low'       : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'high'      : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'increment' : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'threads'   : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'full'      : { 'type': 'bool', 'dashes': 2, 'equal': None  },
            'verbose'   : { 'type': 'bool', 'dashes': 2, 'equal': None  }
        }

        parameter.parseList(params, kwargs)
        self.input     = io(input)
        self.output    = output

        parameter.parseList(params, kwargs)
        parameter.parse( 'output', 'file',  2,      True,  self.output )
        parameter.parse( '',       'file',  0,      False, self.input  )


        self.parameter = parameter


        self.inputs    = [ self.input  ]
        self.outputs   = [ self.output ]

        print "  INITING JELLY HISTO CMD " + self.parameter.getCmd()
        print "    INPUTS : " + str(self.inputs)
        for inp in self.inputs:
            print str(inp) + "\n"
            
        print "    OUTPUTS: " + str(self.outputs)
        for out in self.outputs:
            print str(out) + "\n"





class jellyDump(sampleWrapper):
    def __init__(self, input=None, _name=None, **kwargs):
        """
        Usage: jellyfish stats [options] db:path

        Dump k-mer counts

        By default, dump in a fasta format where the header is the count and
        the sequence is the sequence of the k-mer. The column format is a 2
        column output: k-mer count.

        Options (default value in (), *required):
         -c, --column                             Column format (false)
         -t, --tab                                Tab separator (false)
         -L, --lower-count=uint64                 Don't output k-mer with count < lower-count
         -U, --upper-count=uint64                 Don't output k-mer with count > upper-count
         -o, --output=c_string                    Output file
             --usage                              Usage
         -h, --help                               This message
         -V, --version                            Version
        """
        assert input  is not None
        assert _name  is not None
        function  = "dump"
        nickName  = className + "_" + function + "_" + _name
        print "  INITING JELLY " + function.upper() + " " + nickName
        sampleWrapper.__init__(self, nickName)
        self.input    = input
        self.function = function
        self.nickName = nickName
        self.name     = _name
        self.kwargs   = kwargs

    def getInput(self):
        return self.input

    def getOutput(self):
        return self.output

    def __call__(self, messaging):
        #print "using correct call"
        self.initChild()
        if not io(self.outputs).exists():
            print "RUNNING"
            sampleWrapper.__call__(self, messaging)
        else:
            print "SKIPPING"
            #print "error. no command to run"
            messaging.status = constants.SKIPPED
            print "RETURNING STATUS "     + str(messaging.status)
            print "EXIT STATUS ORIGINAL " + str(messaging.exitCode)
            messaging.exitCode = 0
            print "EXIT STATUS NEW "      + str(messaging.exitCode)

    def initChild(self):
        #print "RUNNING RIGHT INIT CHILD"
        input    = self.input
        name     = self.name
        kwargs   = self.kwargs
        function = self.function
        nickName = self.nickName

        output = kwargs.get('output', None)
        if output is None:
            output          = input + ".fasta"

        parameter = parameters()
        parameter.append(exe,           True,   'name')
        parameter.append(function,      True,   'name')

        params = {
            'column'          : { 'type': 'bool', 'dashes': 2, 'equal': None  },
            'tab'             : { 'type': 'bool', 'dashes': 2, 'equal': None  },
            'lower-count'     : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'upper-count'     : { 'type': 'num',  'dashes': 2, 'equal': True  },
        }

        parameter.parseList(params, kwargs)
        self.input     = io(input)
        self.output    = output

        parameter.parseList(params, kwargs)
        parameter.parse( 'output', 'file',  2,      True,  self.output )
        parameter.parse( '',       'file',  0,      False, self.input  )


        self.parameter = parameter


        self.inputs    = [ self.input  ]
        self.outputs   = [ self.output ]

        print "  INITING JELLY DUMP CMD " + self.parameter.getCmd()
        print "    INPUTS : " + str(self.inputs)
        for inp in self.inputs:
            print str(inp) + "\n"
            
        print "    OUTPUTS: " + str(self.outputs)
        for out in self.outputs:
            print str(out) + "\n"





class jellyMerge(sampleWrapper):
    def __init__(self, input=None, _name=None, **kwargs):
        """
        Usage: jellyfish merge [options] input:c_string+

        Merge jellyfish databases

        Options (default value in (), *required):
        -s, --buffer-size=Buffer length          Length in bytes of input buffer (10000000)
        -o, --output=string                      Output file (mer_counts_merged.jf)
            --out-counter-len=uint32             Length (in bytes) of counting field in output (4)
            --out-buffer-size=uint64             Size of output buffer per thread (10000000)
        -v, --verbose                            Be verbose (false)
            --usage                              Usage
        -h, --help                               This message
        -V, --version                            Version
        """
        assert input  is not None
        assert _name  is not None
        function  = "merge"
        nickName  = className + "_" + function + "_" + _name
        print "  INITING JELLY " + function.upper() + " " + nickName
        sampleWrapper.__init__(self, nickName)
        self.input    = input
        self.function = function
        self.nickName = nickName
        self.name     = _name
        self.kwargs   = kwargs

    def getInput(self):
        return self.input

    def getOutput(self):
        return io(self.output)

    def __call__(self, messaging):
        #print "using correct call"
        self.initChild()
        if not io(self.outputs).exists():
            print "RUNNING"
            sampleWrapper.__call__(self, messaging)
        else:
            print "SKIPPING"
            #print "error. no command to run"
            messaging.status = constants.SKIPPED
            print "RETURNING STATUS "     + str(messaging.status)
            print "EXIT STATUS ORIGINAL " + str(messaging.exitCode)
            messaging.exitCode = 0
            print "EXIT STATUS NEW "      + str(messaging.exitCode)

    def initChild(self):
        #print "RUNNING RIGHT INIT CHILD"
        input    = self.input
        name     = self.name
        kwargs   = self.kwargs
        function = self.function
        nickName = self.nickName


        output = kwargs.get('output', None)
        if output is None:
            output          = input + "_mer_counts"

        parameter = parameters()
        parameter.append(exe,           True,   'name')
        parameter.append(function,      True,   'name')

        params = {
            'buffer-size'     : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'out-counter-len' : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'out-buffer-size' : { 'type': 'num',  'dashes': 2, 'equal': True  },
            'verbose'         : { 'type': 'bool', 'dashes': 2, 'equal': None  }
        }

        parameter.parseList(params, kwargs)
        self.input     = io(input)
        self.output    = output

        parameter.parseList(params, kwargs)
        parameter.parse( 'output', 'file',  2,      True,  self.output )
        parameter.parse( '',       'file',  0,      False, self.input  )


        self.parameter = parameter


        self.inputs    = [ self.input  ]
        self.outputs   = [ self.output ]

        print "  INITING JELLY MERGE CMD " + self.parameter.getCmd()
        print "    INPUTS : " + str(self.inputs)
        for inp in self.inputs:
            print str(inp) + "\n"
            
        print "    OUTPUTS: " + str(self.outputs)
        for out in self.outputs:
            print str(out) + "\n"






if __name__ == "__main__":
    fn = '/mnt/nexenta/aflit001/nobackup/Data/F5/F5_Illumina/F5_Illumina_GOG18L3_pairedend_300/110126_SN132_B_s_3_1_seq_GOG-18.fastq'
    ou = '/tmp/110126_SN132_B_s_3_1_seq_GOG-18.fastq'
    #count = jellyCount(input=None, output=None, buffer_size=None, out_counter_len=4, out_buffer_size=10000000, verbose=False)
    count  = jellyCount(fn,         output=ou,   buffer_size=1000, out_counter_len=4, out_buffer_size=10000000, verbose=False)
    print count.cmd
    count  = jellyCount(fn,         output=ou,                                                                  verbose=True)
    print count.cmd
    count  = jellyCount(fn)
    print count.cmd



"""
count, stats, histo, dump, merge, query, cite, qhisto, qdump, qmerge, jf



COUNT
Usage: jellyfish count [options] file:path+

Count k-mers or qmers in fasta or fastq files

Options (default value in (), *required):
 -m, --mer-len=uint32                    *Length of mer
 -s, --size=uint64                       *Hash size
 -t, --threads=uint32                     Number of threads (1)
 -o, --output=string                      Output prefix (mer_counts)
 -c, --counter-len=Length in bits         Length of counting field (7)
     --out-counter-len=Length in bytes    Length of counter field in output (4)
 -C, --both-strands                       Count both strand, canonical representation (false)
 -p, --reprobes=uint32                    Maximum number of reprobes (62)
 -r, --raw                                Write raw database (false)
 -q, --quake                              Quake compatibility mode (false)
     --quality-start=uint32               Starting ASCII for quality values (64)
     --min-quality=uint32                 Minimum quality. A base with lesser quality becomes an N (0)
 -L, --lower-count=uint64                 Don't output k-mer with count < lower-count
 -U, --upper-count=uint64                 Don't output k-mer with count > upper-count
     --matrix=Matrix file                 Hash function binary matrix
     --timing=Timing file                 Print timing information
     --stats=Stats file                   Print stats
     --usage                              Usage
 -h, --help                               This message
     --full-help                          Detailed help
 -V, --version                            Version





STATS
Usage: jellyfish stats [options] db:path

Statistics

Display some statistics about the k-mers in the hash:

Unique:    Number of k-mers which occur only once.
Distinct:  Number of k-mers, not counting multiplicity.
Total:     Number of k-mers, including multiplicity.
Max_count: Maximum number of occurrence of a k-mer.

Options (default value in (), *required):
 -L, --lower-count=uint64                 Don't consider k-mer with count < lower-count
 -U, --upper-count=uint64                 Don't consider k-mer with count > upper-count
 -v, --verbose                            Verbose (false)
 -o, --output=c_string                    Output file
     --usage                              Usage
 -h, --help                               This message
     --full-help                          Detailed help
 -V, --version                            Version




HISTO
Usage: jellyfish histo [options] db:path

Create an histogram of k-mer occurrences

Create an histogram with the number of k-mers having a given
count. In bucket 'i' are tallied the k-mers which have a count 'c'
satisfying 'low+i*inc <= c < low+(i+1)*inc'. Buckets in the output are
labeled by the low end point (low+i*inc).

The last bucket in the output behaves as a catchall: it tallies all
k-mers with a count greater or equal to the low end point of this
bucket.

Options (default value in (), *required):
 -l, --low=uint64                         Low count value of histogram (1)
 -h, --high=uint64                        High count value of histogram (10000)
 -i, --increment=uint64                   Increment value for buckets (1)
 -t, --threads=uint32                     Number of threads (1)
 -f, --full                               Full histo. Don't skip count 0. (false)
 -o, --output=c_string                    Output file
 -v, --verbose                            Output information (false)
     --usage                              Usage
     --help                               This message
     --full-help                          Detailed help
 -V, --version                            Version




DUMP
Usage: jellyfish stats [options] db:path

Dump k-mer counts

By default, dump in a fasta format where the header is the count and
the sequence is the sequence of the k-mer. The column format is a 2
column output: k-mer count.

Options (default value in (), *required):
 -c, --column                             Column format (false)
 -t, --tab                                Tab separator (false)
 -L, --lower-count=uint64                 Don't output k-mer with count < lower-count
 -U, --upper-count=uint64                 Don't output k-mer with count > upper-count
 -o, --output=c_string                    Output file
     --usage                              Usage
 -h, --help                               This message
 -V, --version                            Version



MERGE
Usage: jellyfish merge [options] input:c_string+

Merge jellyfish databases

Options (default value in (), *required):
 -s, --buffer-size=Buffer length          Length in bytes of input buffer (10000000)
 -o, --output=string                      Output file (mer_counts_merged.jf)
     --out-counter-len=uint32             Length (in bytes) of counting field in output (4)
     --out-buffer-size=uint64             Size of output buffer per thread (10000000)
 -v, --verbose                            Be verbose (false)
     --usage                              Usage
 -h, --help                               This message
 -V, --version                            Version


"""
