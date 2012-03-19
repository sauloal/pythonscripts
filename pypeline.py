#!/usr/bin/python
import os
import sys

try:
    #import yaml
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


from techs    import *
from wrappers import *
from tools    import *
from tools    import constants

import setup


jellyParams = { 'buffer_size':    1000,
                'out_counter_len':4,
                'out_buffer_size':10000000,
                'verbose':        False }


sw = sampleWrapper.sampleWrapper("watever0")
f0 = joblaunch.Job('f0', [sw                      ], selfTester=sw )
f1 = joblaunch.Job('f1', [sampleWrapper.sample    ], deps=[f0] )


data = {'f0': f0,
        'f1': f1}

print "DATASET\n" + str(setup.ldataset)

for lib in setup.ldataset:
    print 'LIB ' + lib.getName()
    for pair in lib:
        print '  PAIR ' + pair.getName() + ' TYPE ' + pair.getType()
        pairChildren = []
        for run in pair:
            print '    RUN ' + run.getShortName()
            print '    FN  ' + run.getFileName()
            jellyPipe = jelly.getJellyPipeline(run.getFileName(), '/tmp', None, 'pipetest', None, **jellyParams)
            children.append(jellyPipe)






#TODO. MUST HAVE A __RUN__ FUNCTION TO BE CALLED WHEN RUN. CANT BE SENT INSTANTIATED
#FUNCTION ANYMORE DUE TO PICLKING

#                  ID,   COMMAND                      SELFTEST=               DEPS=


#fn        = '/mnt/nexenta/aflit001/nobackup/Data/F5/F5_Illumina/F5_Illumina_GOG18L3_pairedend_300/110126_SN132_B_s_3_1_seq_GOG-18.fastq'
#jellyPipe = jelly.getJellyPipeline(fn, '/tmp', None, 'pipetest', **jellyParams)



all=[sw, data]

if useYaml:
    dataDump = str(dump(data, Dumper=Dumper))
    #print dataDump
    data2    = load(dataDump, Loader=Loader)


joblaunch.mainLib(data2, verbose=True, justPrint=True)


#joblaunch.mainLib(data, verbose=True)
