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


class jellyCount():
    def __init__(self, name, input, buffer_size=10000000, output="mer_counts_merged.jf", out_counter_len=4, out_buffer_size=10000000, verbose=False):
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
        
class jellyStats():
    def __init__(self, input, lower_count=None, upper_count=None, output="-", verbose=False):
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

class jellyHisto():
    def __init__(self, input, low=1, high=10000, increment=1, threads=1, full=False, output="-", verbose=False):
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


class jellyMerge():
    def __init__(self, input, column=False, tab=False, lower_count=None, upper_count=None):
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
