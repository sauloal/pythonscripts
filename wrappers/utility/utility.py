#!/usr/bin/python
#-*- coding: UTF-8 -*-

"""
This is the main file of this utility workflow program.
The idea is that you write a number of 'plugins' which should all have a
'main' method.
With this you write a configuration file, specifying the plugin to call,
the order in which to call them and the parameter used for each of them.
This file will read the configuration file and call all the plugins you
asked with the parameter you defined.


(c) Copyright Pierre-Yves Chibon -- 2009-2012

Distributed under License GPLv3 or later
You can find a copy of this license on the website
http://www.gnu.org/licenses/gpl.html

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
   
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
   
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""

import ConfigParser
import csv
import logging
import os
import sys
from Conf import Conf, ConfError
from optparse import OptionParser
from  FileIO import FileIO


def getArgument():
    """ Retrieve command line argument. """
    parser = OptionParser(version="%prog 1.0")
    parser.add_option("-c", "--config", dest="config", default=None,
                type="string",
                help="Configuration file to use.")
    parser.add_option("-m", "--module", dest="module", default=None,
                type="string",
                help="Module to run (if there is only one to run)")
    parser.add_option("-f", "--file", dest="inputFile", default=None,
                type="string",
                help="The input file (text file with the value separated \
                by a semi-colon';') ")
    parser.add_option("-d", "--delimiter", dest="delimiter",
                type="string", default=None,
                help="The delimiter of the input file (Default =';')")
    (options, args) = parser.parse_args()

    return (options.config, options.module, options.inputFile, options.delimiter)


class UtilityError(Exception):
    """ Basic exception class to be used in the project. """
    pass


class Utility:
    """ This is the main class of the program.
    It retrieves the configuration file passed to the program, load the
    mentioned plugin with the specified parameters and go on with the
    pipeline.
    """
    def __init__(self, args):
        """ Constructors.
        :arg args, the command line parameter passed to the program.
        """
        (conffile , module , inputfile , delimiter ) = args
        self.conffile = conffile
        self.conf = None
        self.modules = None
        self.inputfile = inputfile
        self.delimiter = delimiter
        self.optionsmod = {}
        self.log = logging.getLogger('utility')
        
    def handleWritting(self, matrix, options):
        """
        Handle the writting to a file of the list called matrix and
        given as parameter
        """
        if any(x for x in options.keys() if x in ('output', 'output1' ,
            'output2' )) and !isinstance(matrix, int):
            if isinstance(matrix, list):
                outputfile = None
                # Set the name of the output file in the correct directory
                if self.filedir.endswith('/'):
                    outputfile = self.filedir + options['output']
                else:
                    outputfile = self.filedir + '/' + options['output']
                # write the file :)
                output = FileIO(outputfile, self.delimiter)
                output.writeFile(matrix)
            else:
                i = 0
                for m in matrix:
                    i = i + 1 
                    try:
                        filename = options['output'+str(i)]
                    except KeyError, err:
                        raise ('The options "%s" is not defined, \
                        please correct this \n %s -- %s \n %s' % (
                        'output'+str(i), len(matrix), type(matrix),
                        options) )
                    
                    if self.filedir.endswith('/'):
                        outputfile = self.filedir + filename
                    else:
                        outputfile = self.filedir + '/' + filename
                    # write the file :)
                    output = FileIO(outputfile, self.delimiter)
                    output.writeFile(matrix[i-1])


    def main(self):
        """
        Retreive the information from the config file
        Load the first class
        Load its second output if required in the config file
        Set its argument
        Sent the 'readers' -> files
        Run the main function of the class
        Store one output if there are several back
        Go to the next class
        """
        if not self.conf:
            raise UtilityError('No configuration file specified')
        self.log.info('Using configuration file: %s' % self.conffile)
        self.conf = Conf(self.conffile)
        self.modules = self.conf.getModules(None)
        
        # Retrive the main options
        try:
            self.optionsmod['General'] = self.conf.getSection('General')
        except  ConfigParser.NoSectionError, err:
            self.log.debug('The section "General" does not exist or has \
            no option set')

        try:
            self.filedir = self.optionsmod['General']['filedir']
        except KeyError, err:
            self.log.debug('No file identified')
        try:
            self.delimiter = self.optionsmod['General']['delimiter']
        except KeyError, err:
            self.log.debug('no delimiter found')

        # Check if the plugins asked are present
        ext = 0
        for mod in self.modules.values():
            if mod not in os.listdir('./plugins'):
                self.log.info(' * The plugin is not present : %s' %mod)
                ext = 1
        # If one the plugin is missing crash...
        if ext:
            raise UtilityError('The analysis could not be perform -- \
                see error above')

        # Retrieve the options for each module
        for mod in self.modules.keys():
            try:
                self.optionsmod[mod] = self.conf.getSection(str(mod))
            except  ConfigParser.NoSectionError, err:
                self.log.debug('The section %s (%s) does not exist or \
                has no option set' % (mod, self.modules[mod]))

        if self.optionsmod['General']['file'] not in os.listdir(self.filedir):
            raise UtilityError( 'The file %s is not present in the folder \
            %s' % (self.optionsmod['General']['file'], self.filedir))
            

        # Open the file and create the reader object to send to the first plugin
        if self.filedir.endswith('/'):
            inputfile = self.filedir + self.optionsmod['General']['file']
        else:
            inputfile = self.filedir + '/' + self.optionsmod['General']['file']
        
        matrix = FileIO(inputfile , delimiter= self.delimiter ).readFile()

        # Load the module, create the object, give it the options and run it :-)
        for mod in self.modules.keys():
            moduleName = self.modules[mod]
            self.log.info( '\n * %s' % moduleName)
                        
            # if the module has a specific input file transform the matrix in tuple
            try:
                inputfile = self.optionsmod[mod]['inputfile'].split(',')
                print "Add file(s):\n '%s'" % "'\n'".join(inputfile).strip()
                self.log.info( 'Add file(s):\n "%s"' % '\n'.join(
                    inputfile).strip())
                for file in inputfile:
                    m2 = FileIO(file.strip(), 
                        delimiter=self.delimiter).readFile()
                    if isinstance(matrix, tuple):
                        matrix = [el for el in matrix]
                        matrix.append(m2)
                    else:
                        matrix = (matrix, m2)
            except KeyError, err: 
                self.log.debug('No %s set' %err)
            
            # if the module has a specific input file transform the matrix in tuple
            try:
                if int(self.optionsmod[mod]['nr_input']) != len(matrix):
                    sys.exit('The input requested/given is not correct \
                    \n %s vs %s ' % (self.optionsmod[mod]['nr_input'],
                    len(matrix)))
            except KeyError, err: 
                self.log.debug('No %s set' %err)
                
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
                self.log.debug('No %s set' %err)
            except AttributeError, err:
                self.log.info('The object %s has no method "setOptions"\
                ' % mod)

            # Run the plugin
            matrix = obj.main(matrix)

            # Should the ouput be written down ?
            try:
                if int(self.optionsmod[mod]['write']) == 1:
                    ind = int(self.optionsmod[mod]['writematrix'])
                    self.handleWritting(matrix[ind], self.optionsmod[mod])
            except KeyError, err: 
                self.log.debug('No %s set' %err)
            
            # If the matrix is a tuple which part should be kept ?
            try:
                ind = int(self.optionsmod[mod]['keep'])
                matrix = matrix[ind]
            except KeyError, err: 
                self.log.debug('No %s set' %err)

        self.log.info('Final ouput :')
        self.handleWritting(matrix, self.optionsmod['General'])


if __name__ == "__main__": 

    # Check the structure of the application
    if 'plugins' not in os.listdir('.') or not os.path.isdir('plugins'):
        print 'The folder "plugins" does not exist in the current directory'
    else:
        try:
            ut = Utility(getArgument())
            ut.main()
        except UtilityError, err:
            print 'ERROR:', err
        except ConfError, err:
            print 'CONF ERROR', err
