#!/usr/bin/python
#-*- coding: UTF-8 -*-

# For a given column replace the letters by thier numbers

#*****************************************************
#
#  (c) Copyright Pierre-Yves Chibon -- 2009
#
#   Distributed under License GPLv3 or later
#   You can find a copy of this license on the website
#   http://www.gnu.org/licenses/gpl.html
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#       
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#       
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#   MA 02110-1301, USA.
#
#*****************************************************

import sys

list = []
nogood = []

class replaceReplicates:

    def __init__(self):
        self.replicates = None
        self.column = None
        self.delimiter = None
    
    def setOptions(self, opt):
        self.column = int(opt['column']) -1
        self.replicates = opt['replicates']
        self.delimiter = opt['delimiter']
    
    def main(self, reader):
        
        # If the input file is not specified
        if not reader:
            sys.exit("\n***  Please define one input file  ***\n")
        
        if not self.replicates:
            self.replicates = ['a', 'b', 'c', 'd']
        else:
            self.replicates = self.replicates.split(',')

    
        lineNum = 0
        name = None
        for row in reader: 
            # count the number of line in the file
            lineNum = lineNum + 1
            # First line contains the header -> Direct to the output
            if lineNum == 1:
                tmp = [el for el in row]
                print self.column
                tmp[self.column] = 'Replicate'
                list.append(tmp)
            else:
                # If the row is not empty
                if row != None and row != []:
                    # If the first element is not empty
                    if row[0] != None and row[0].strip() != '':
                        tmp = [el for el in row]
                        tmp[self.column] = self.replicates.index(tmp[self.column].lower()) + 1
                        list.append(tmp)
        
        print " *** %d lignes has been read ***" %(lineNum)

        return list
