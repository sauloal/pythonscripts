#!/usr/bin/python
#-*- coding: UTF-8 -*-

import os, csv
from types import *

class FileIO:
    """
        This class handles the FileIO part
    """
    
    def __init__(self, filename, delimiter = None):
        self.filename = filename
        self.delimiter = delimiter
    
    def readFile(self):
        '''
            This methods reads the file defined by self.filename using the delimiter self.delimiter
        '''
        if self.delimiter:
            reader = csv.reader(open(self.filename, "rb"), delimiter = self.delimiter)
        else:
            reader = open(self.filename, "rb")
        # To be able to send the same matrix several time it has to be saved on the memory first
        matrix = []
        for row in reader:
            matrix.append(row)
        
        return matrix
    
    def writeFile(self, list, append = False):
        '''
            This method writes a CSV file with the name self.filename, the delimiter self.delimiter and
            with the content given as parameter.
            The content is the list of rows. It checks if all element of the list are list as well
            if it is then it writes it to the file with the delimiter given else it happens the string directly.
        '''
        if len(list) != 0:
            try:
                if append:
                    print 'Append'
                    f = open(self.filename, 'a')
                else:
                    print 'Write'
                    f = open(self.filename, 'w')
                for l in list:
                    # If the content of this list is a list (true for the values -- false for the header line)
                    if type(l) is ListType or type(l) is TupleType:
                        string = ''
                        pos = 0
                        for el in l:
                            pos = pos + 1
                            string += '"%s"' %str(el)
                            if pos != len(l):
                                string += self.delimiter
                        f.write(string)
                    # Concerns only the header line
                    else:
                        f.write(l)
                    f.write('\n')
                f.close()
            except Exception, e:
                print 'Error while writing %s' %(self.filename)
                print e
            else:
                print ' *** %s values are in the file : %s' %(len(list), self.filename)
    
    def writeFasta(self, list):
        ''' 
            This method writes a Fasta file with the name self.filename and the content given as parameter.
            The content is a list of sequences with their name and their sequences.
        '''
        if len(list) != 0:
            try:
                f = open(self.filename, 'w')
                for sequence in list:
                    if not sequence.name.startswith('>'):
                        string = "> %s" %sequence.name
                        f.write(string)
                    else:
                        f.write(sequence.name)
                    f.write('\n')
                    f.write(str(sequence.sequence))
                    f.write('\n')
                f.close()
            except Exception, e:
                print 'ERROR while writing : %s' %(self.filename)
                print e
            else:
                print ' *** %s sequences are in the file : %s' %(len(list), self.filename)
            
