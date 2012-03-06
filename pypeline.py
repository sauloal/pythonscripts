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

import setup





print "DATASET\n" + str(setup.ldataset)

for lib in setup.ldataset:
    print 'LIB ' + lib.getName()
    for pair in lib:
        print '  PAIR ' + pair.getName() + ' TYPE ' + pair.getType()
        for run in pair:
            print '    RUN ' + run.getShortName()


            
sw = sampleWrapper.sampleWrapper("watever0")
#TODO. MUST HAVE A __RUN__ FUNCTION TO BE CALLED WHEN RUN. CANT SENT INSTANTIATED 
#FUNCTION ANYMORE DUE TO PICLKING
#                  ID,   COMMAND                      SELFTEST=               DEPS=
f0 = joblaunch.Job('f0', [sampleWrapper.sampleWrapper     ] )
#f0 = joblaunch.Job('f0', [sampleWrapper.sample     ] )
#f0 = joblaunch.Job('f0', [sw                      ] )
#f0 = joblaunch.Job('f0', [['sleep 55;', 'echo f0']] )
f1 = joblaunch.Job('f1', [['sleep 55;', 'echo f1']], deps=[f0] )
f2 = joblaunch.Job('f2', [['sleep 34;', 'echo f2']], deps=[f0] )
f3 = joblaunch.Job('f3', [['sleep 21;', 'echo f3']], deps=[f0] )
l1 = joblaunch.Job('l1', [['sleep 13;', 'echo l1']], deps=[f1, f2, f3] )
f4 = joblaunch.Job('f4', [['sleep  8;', 'echo f4']], deps=[f0] )
f5 = joblaunch.Job('f5', [['sleep  5;', 'echo f5']], deps=[f0] )
f6 = joblaunch.Job('f6', [['sleep  3;', 'echo f6']], deps=[f0] )
l2 = joblaunch.Job('l2', [['sleep  2;', 'echo l2']], deps=[f4, f5, f6] )
d1 = joblaunch.Job('d1', [['sleep  1;', 'echo d1']], deps=[l1, l2] )

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



#str   = str(dump(data, Dumper=Dumper))
#print str
#data2 = load(str, Loader=Loader)
#joblaunch.mainLib(data2, verbose=True)


joblaunch.mainLib(data, verbose=True)
