#!/usr/bin/python
#-*- coding: UTF-8 -*-

# Extract the legend and the desired column from a csv file

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

class removeColumn:

    def __init__(self):
        self.start = None
        self.column = None
        self.delimiter = None
    
    def setOptions(self, opt):
        self.start = int(opt['start'])
        self.column = int(opt['column']) -1
        self.delimiter = opt['delimiter']
    
    def main(self, reader):
        
        if self.column < self.start:
            sys.exit("\n***  The column to retrieve is included in the legend please change this !  ***\n")
        
        # If the input file is not specified
        if not reader:
            sys.exit("\n***  Please define one input file  ***\n")

        lineNum = 0
        name = None
        for row in reader: 
            # count the number of line in the file
            lineNum = lineNum + 1
            # First line contains the header -> Direct to the output
            if lineNum == 1:
                tmp = [el for el in row[0:self.start]]
                # Obs is the name used for the java application
                tmp.append('Obs')
                name = row[self.column]
                list.append(tmp)
            else:
                # If the row is not empty
                if row != None and row != []:
                    # If the first element is not empty
                    if row[0] != None and row[0].strip() != '':
                            tmp = [el for el in row[0:self.start]]
                            tmp.append(row[self.column])
                            list.append(tmp)
        
        print " *** %d lignes has been read ***" %(lineNum)

        return list
