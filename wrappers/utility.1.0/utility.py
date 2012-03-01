#!/usr/bin/python
#-*- coding: UTF-8 -*-

from Conf import Conf
import os, sys, ConfigParser, csv
from optparse import OptionParser
from types import *
from  FileIO import FileIO

### arguments
# retrieve the arguments given and show the help when needed
def getArgument():
    # Handle the parameters
    parser = OptionParser(version="%prog 1.0")
    parser.add_option("-c", "--config", dest="config", default=None, type="string",
                  help="Configuration file to use.")
    parser.add_option("-m", "--module", dest="module", default=None, type="string",
                  help="Module to run (if there is only one to run)")
    parser.add_option("-f", "--file", dest="inputFile", default=None, type="string",
                  help="The input file (text file with the value separated by a semi-colon';') ")
    parser.add_option("-d", "--delimiter", dest="delimiter", type="string", default=None,
                  help="The delimiter of the input file (Default =';')")
                  
    (options, args) = parser.parse_args()

    return (options.config, options.module, options.inputFile, options.delimiter)

class Utility:

    def __init__(self, args):
        (conffile , module , inputfile , delimiter ) = args
        self.conffile = None #Conf(conffile)
        self.modules = None #self.connffile.getModules(None)
        self.inputfile = inputfile
        self.delimiter = delimiter
        self.optionsmod = {}
        
    def handleWritting(self, matrix, options):
        '''
        Handle the writting to a file of the list called matrix and given as parameter
        '''
        if any(x for x in options.keys() if x in ('output', 'output1' , 'output2' )) \
        and type(matrix) != IntType:
            if type(matrix) == ListType:
                outputfile = None
                # Set the name of the output file in the correct directory
                if self.filedir.endswith('/'):
                    outputfile = self.filedir + options['output']
                else:
                    outputfile = self.filedir + '/' + options['output']
                # write the file :)
                #print '**** %s' %outputfile
                output = FileIO(outputfile, self.delimiter)
                output.writeFile(matrix)
            else:
                i = 0
                for m in matrix:
                    #print len(m)
                    i = i + 1 
                    try:
                        #print options
                        filename = options['output'+str(i)]
                    except KeyError, err:
                        sys.exit( 'The options "%s" is not defined, please correct this \n %s -- %s \n %s' %('output'+str(i), len(matrix), type(matrix), options) )
                    
                    if self.filedir.endswith('/'):
                        outputfile = self.filedir + filename
                    else:
                        outputfile = self.filedir + '/' + filename
                    # write the file :)
                    output = FileIO(outputfile, self.delimiter)
                    output.writeFile(matrix[i-1])


    def main(self):
        '''
        Retreive the information from the config file
        Load the first class
        Load its second output if required in the config file
        Set its argument
        Sent the 'readers' -> files
        Run the main function of the class
        Store one output if there are several back
        Go to the next class
        '''
        conf = './conf/MN-Ali-RunMod2.conf'
        #conf = './conf/2003VE.conf'
        #conf = './conf/toDB-CE03.conf'
        print "*** Using the file: '%s' ***" %conf
        self.conffile = Conf(conf)
        self.modules = self.conffile.getModules(None)
        
        # Retrive the main options
        try:
            self.optionsmod['General'] = self.conffile.getSection('General')
            #print self.optionsmod
        except  ConfigParser.NoSectionError, err:
            print 'The section "General" does not exist or has no option set'

        try:
            self.filedir = self.optionsmod['General']['filedir']
        except KeyError, err:
            print 'No file identified'
        try:
            self.delimiter = self.optionsmod['General']['delimiter']
        except KeyError, err:
            print 'no delimiter found'

        # Check if the plugins asked are present
        ext = 0
        for mod in self.modules.values():
            if mod not in os.listdir('./plugins'):
                print ' * The plugin is not present : %s' %mod
                ext = 1
        # If one the plugin is missing crash...
        if ext:
            print ' *** The analysis can not be performed -- see above ** '
            sys.exit('The analysis can not be performed -- see above')

        # Retrieve the options for each module
        for mod in self.modules.keys():
            try:
                #self.optionsmod[self.modules[mod]] = self.conffile.getSection(str(mod))
                self.optionsmod[mod] = self.conffile.getSection(str(mod))
            except  ConfigParser.NoSectionError, err:
                print 'The section %s (%s) does not exist or has no option set' %(mod, self.modules[mod])

        if self.optionsmod['General']['file'] not in os.listdir(self.filedir):
            sys.exit('The file %s is not present in the folder %s'\
            %(self.optionsmod['General']['file'], self.filedir))
            

        # Open the file and create the reader object to send to the first plugin
        if self.filedir.endswith('/'):
            inputfile = self.filedir + self.optionsmod['General']['file']
        else:
            inputfile = self.filedir + '/' + self.optionsmod['General']['file']
        
        matrix = FileIO(inputfile , delimiter= self.delimiter ).readFile()

        # Load the module, create the object, give it the options and run it :-)
        #for mod in self.modules.values():
        for mod in self.modules.keys():
            moduleName = self.modules[mod]
            print '\n *', moduleName
                        
            # if the module has a specific input file transform the matrix in tuple
            try:
                inputfile = self.optionsmod[mod]['inputfile'].split(',')
                print "Add file(s):\n '%s'" % "'\n'".join(inputfile).strip()
                for file in inputfile:
                    m2 = FileIO(file.strip() , delimiter = self.delimiter ).readFile()
                    if type(matrix) is TupleType:
                        #print 'added'
                        matrix = [el for el in matrix]
                        matrix.append(m2)
                    else:
                        #print 'created'
                        matrix = (matrix, m2)
            except KeyError, err: 
                print 'No %s set' %err 
                #pass
            
            # if the module has a specific input file transform the matrix in tuple
            try:
                if int(self.optionsmod[mod]['nr_input']) != len(matrix):
                    sys.exit('The input requested/given is not correct \n %s vs %s ' %(self.optionsmod[mod]['nr_input'], len(matrix)))
            except KeyError, err: 
                print 'No %s set' %err 
                #pass
                
            # Load the module
            modname = moduleName.split('.py')[0]
            m = __import__('plugins.%s'%modname)
            m = getattr(m, modname)
            object = getattr(m, modname)
            
            # Create the object
            obj = object()
            
            # Set the options
            try:
                obj.setOptions(self.optionsmod[mod])
            except KeyError, err:
                #print "The object %s has no options set specificaly -- %s" %(mod, optionsmod)
                pass
            except AttributeError, err:
                print "The object %s has no method 'setOptions'" %mod
            
            ##################
            # Run the function
            matrix = obj.main(matrix)
            ##################

            # Should the ouput be written down ?
            try:
                if int(self.optionsmod[mod]['write']) == 1:
                    ind = int(self.optionsmod[mod]['writematrix'])
                    self.handleWritting(matrix[ind], self.optionsmod[mod])
            except KeyError, err: 
                #print 'No %s set' %err 
                pass
            
            # If the matrix is a tuple which part should be kept ?
            try:
                ind = int(self.optionsmod[mod]['keep'])
                matrix = matrix[ind]
            except KeyError, err: 
                #print 'No %s set' %err 
                pass
        
        print '\n**Final ouput :'
        self.handleWritting(matrix, self.optionsmod['General'])
        

if __name__ == "__main__": 

    # Check the structure of the application
    if 'plugins' not in os.listdir('.') or not os.path.isdir('plugins'):
        sys.exit('The folder "plugins" does not exist in the current directory')
    
    ut = Utility(getArgument())
    ut.main()
