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


sw = sampleWrapper.sampleWrapper("whatever0", cmd="echo whatever0")
f0 = joblaunch.Job('f0', [sw                      ], selfTester=sw )
f1 = joblaunch.Job('f1', [sampleWrapper.sample    ], deps=[f0] )


data = {'f0': f0,
        'f1': f1}

print "DATASET\n" + str(setup.ldataset)
baseChildrenJobs = []
baseChildrenFunc = []

for lib in setup.ldataset:
    print 'LIB ' + lib.getName()
    libChildrenJobs = []
    libChildrenFunc = []
    for pair in lib:
        print '  PAIR ' + pair.getName() + ' TYPE ' + pair.getType()
        pairChildrenJobs = []
        pairChildrenFunc = []
        for run in pair:
            print '    RUN ' + run.getShortName()
            print '    FN  ' + run.getFileName()
            #           getJellyPipeline      (inputFastq=None,  outputFolder=None, prefix=None, suffix=None, dependsOn=[], **kwargs):
            jellyPipe = jellypipe.getJellyPipeline([run.getFileName()], run.getShortName(), '/tmp',           None,        'pipetest',  None,         **jellyParams)

            for jobDesc in jellyPipe:
                data[jobDesc[0]] = jobDesc[1]

#            pairChildrenJobs.append(jellyPipe[1][1])
#            pairChildrenFunc.append(jellyPipe[1][2])
#
#        print "PAIR CHILDREN JOBS " + str(pairChildrenJobs)
#        pairChildrenJobsFiles = []
#        for func in pairChildrenFunc:
#            pairChildrenJobsFiles.append(func.getOutput)
#
#        #def getJellyMergePipeline(    inputJFs=None,          inBaseName=None, outputFolder=None, prefix=None, suffix=None, dependsOn=[],     **kwargs):
#        jellyPairPipe = jellypipe.getJellyMergePipeline(pairChildrenJobsFiles, pair.getName(),  '/tmp',            None,        'pipetest',  pairChildrenJobs, **jellyParams)
#        for jobDesc in jellyPairPipe:
#                data[jobDesc[0]] = jobDesc[1]
#
#        libChildrenJobs.append(jellyPairPipe[0][1])
#        libChildrenFunc.append(jellyPairPipe[0][2])
#
#    print "LIB CHILDREN JOBS " + str(libChildrenJobs)
#    libChildrenJobsFiles = []
#    for func in libChildrenFunc:
#        libChildrenJobsFiles.append(func.getOutput)
#
#    #def getJellyMergePipeline(    inputJFs=None,          inBaseName=None, outputFolder=None, prefix=None, suffix=None, dependsOn=[],     **kwargs):
#    jellyLibPipe = jellypipe.getJellyMergePipeline(libChildrenJobsFiles, lib.getName(),  '/tmp',            None,        'pipetest',  libChildrenJobs, **jellyParams)
#    for jobDesc in jellyLibPipe:
#            data[jobDesc[0]] = jobDesc[1]
#
#    baseChildrenJobs.append(jellyLibPipe[0][1])
#    baseChildrenFunc.append(jellyLibPipe[0][2])
#
#
#print "BASE CHILDREN JOBS " + str(baseChildrenJobs)
#baseChildrenJobsFiles = []
#for func in baseChildrenFunc:
#    baseChildrenJobsFiles.append(func.getOutput)
#
##def getJellyMergePipeline(    inputJFs=None,          inBaseName=None, outputFolder=None, prefix=None, suffix=None, dependsOn=[],     **kwargs):
#jellyBasePipe = jellypipe.getJellyMergePipeline(baseChildrenJobsFiles, setup.ldataset.getName(),  '/tmp',            None,        'pipetest',  baseChildrenJobs, **jellyParams)
#for jobDesc in jellyBasePipe:
#        data[jobDesc[0]] = jobDesc[1]




#TODO. MUST HAVE A __RUN__ FUNCTION TO BE CALLED WHEN RUN. CANT BE SENT INSTANTIATED
#FUNCTION ANYMORE DUE TO PICLKING

#                  ID,   COMMAND                      SELFTEST=               DEPS=


#fn        = '/mnt/nexenta/aflit001/nobackup/Data/F5/F5_Illumina/F5_Illumina_GOG18L3_pairedend_300/110126_SN132_B_s_3_1_seq_GOG-18.fastq'
#jellyPipe = jelly.getJellyPipeline(fn, '/tmp', None, 'pipetest', **jellyParams)



all=[sw, data]

if useYaml:
    #dataDump = str(dump(data, Dumper=Dumper))
    #print dataDump
    pass

#sys.exit(0)
joblaunch.mainLib(data, verbose=True, justPrint=False)


#joblaunch.mainLib(data, verbose=True)
