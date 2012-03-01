#-*- coding: UTF-8 -*-

"""
This file takes care of reading and writting different type of files.
Each almost every plugin as to read of write a file, this avoid code
duplication.

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

import csv
import os

class FileIO:
    """This class handles the FileIO part
    """
    
    def __init__(self, filename, delimiter=None):
        """ Constructor, set the name of the file to read/write.
        :arg filename, the full path to the file to read/write.
        :kwarg delimiter, the delimiter used to separate the values
        in the files (useful for CSV file).
        """
        self.filename = filename
        self.delimiter = delimiter
    
    def readFile(self):
        """This methods reads the file defined by self.filename using
        the delimiter self.delimiter
        """
        if self.delimiter:
            reader = csv.reader(open(self.filename, "rb"),
                delimiter=self.delimiter)
        else:
            reader = open(self.filename, "rb")
        # To be able to send the same matrix several time it has to be
        # saved on the memory first
        matrix = []
        for row in reader:
            matrix.append(row)

        return matrix
    
    def writeFile(self, data, append=False):
        """This method writes a CSV file with the name self.filename,
        the delimiter self.delimiter and with the content given as
        parameter.
        The content is the list of rows. It checks if all element of the
        list are list as well if it is then it writes it to the file
        with the delimiter given else it happens the string directly.
        :arg data, what to write to the file (a list or a list of list
        or simply a text)
        :kwarg append, a boolean specifying if the data should be append
        to the file or if the file should just be (over-)write with this
        data.
        """
        if data:
            try:
                if append:
                    print 'Append'
                    f = open(self.filename, 'a')
                else:
                    print 'Write'
                    f = open(self.filename, 'w')
                if isinstance(data, list) or isinstance(data, tuple):
                    for entry in data:
                        # If the content of this list is a list
                        if isinstance(entry, list) or isinstance(entry, tuple):
                            string = ''
                            pos = 0
                            for el in entry:
                                pos = pos + 1
                                string += '"%s"' %str(el)
                                if pos != len(entry):
                                    string += self.delimiter
                            f.write(string)
                        # Concerns only the header line
                        else:
                            f.write(entry)
                        f.write('\n')
                else:
                    f.write(entry)
                    f.write('\n')
                f.close()
            except Exception, e:
                print 'Error while writing %s' % self.filename
                print e
            else:
                print ' *** %s values are in the file : %s' % (
                    len(data), self.filename)
    
    def writeFasta(self, sequences):
        """This method writes a Fasta file with the name self.filename 
        and the content given as parameter.
        The content is a list of sequences with their name and their
        sequences.
        """
        if sequences:
            try:
                f = open(self.filename, 'w')
                for sequence in sequences:
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
                print 'ERROR while writing : %s' % self.filename
                print e
            else:
                print ' *** %s sequences are in the file : %s' % (
                    len(sequences), self.filename)
            
