#!/usr/bin/python
import os

import yaml
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
    print "USING YAML C VERSION"
except ImportError:
    from yaml import Loader, Dumper
    print "USING YAML PYTHON VERSION"


from techs    import *
from wrappers import *
from tools    import *
from tools    import constants

import setup





print "DATASET\n" + str(setup.ldataset)

for lib in setup.ldataset:
    print 'LIB ' + lib.getName()
    for pair in lib:
        print '  PAIR ' + pair.getName() + ' TYPE ' + pair.getType()
        for run in pair:
            print '    RUN ' + run.getShortName()


            
sw         = sampleWrapper.sampleWrapper("watever0")

fn         = '/mnt/nexenta/aflit001/nobackup/Data/F5/F5_Illumina/F5_Illumina_GOG18L3_pairedend_300/110126_SN132_B_s_3_1_seq_GOG-18.fastq'
ou         = '/tmp/110126_SN132_B_s_3_1_seq_GOG-18.fastq'
jellyCount = jelly.jellyCount(fn,         output=ou,   buffer_size=1000, out_counter_len=4, out_buffer_size=10000000, verbose=False)

#TODO. MUST HAVE A __RUN__ FUNCTION TO BE CALLED WHEN RUN. CANT BE SENT INSTANTIATED 
#FUNCTION ANYMORE DUE TO PICLKING

#                  ID,   COMMAND                      SELFTEST=               DEPS=


f0 = joblaunch.Job('f0', [sw                      ], selfTester=sw )
f1 = joblaunch.Job('f1', [sampleWrapper.sample    ], deps=[f0] )
f2 = joblaunch.Job('f2', [jellyCount              ], deps=[f0] )
#f2 = joblaunch.Job('f2', [['sleep  3;', 'echo f2']], deps=[f0] )
f3 = joblaunch.Job('f3', [['sleep  4;', 'echo f3']], deps=[f0] )
l1 = joblaunch.Job('l1', [['sleep  5;', 'echo l1 err;', 'exit 1']], deps=[f1, f2, f3] )
f4 = joblaunch.Job('f4', [['sleep  6;', 'echo f4']], deps=[f0] )
f5 = joblaunch.Job('f5', [['sleep  7;', 'echo f5']], deps=[f0] )
f6 = joblaunch.Job('f6', [['sleep  8;', 'echo f6']], deps=[f0] )
l2 = joblaunch.Job('l2', [['sleep  9;', 'echo l2']], deps=[f4, f5, f6] )
d1 = joblaunch.Job('d1', [['sleep 10;', 'echo d1']], deps=[l1, l2] )

data = {'f0': f0,
        'f1': f1,
        'f2': f2,
        'f3': f3,
        'l1': l1,
        'f4': f4,
        'f5': f5,
        'f6': f6,
        'l2': l2,
        'd1': d1}

all=[sw, data]



dataDump = str(dump(data, Dumper=Dumper))
print dataDump
data2 = load(dataDump, Loader=Loader)
joblaunch.mainLib(data2, verbose=True)


#joblaunch.mainLib(data, verbose=True)
