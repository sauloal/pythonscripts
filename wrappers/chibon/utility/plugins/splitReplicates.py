#!/usr/bin/python
#-*- coding: UTF-8 -*-

# Split the replicates from a given column.
# default replicates being a,b,c,d
# default split on is ' '~\s

# replicate in the conf file
# replicate = a,b,c,d,e,f

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

class splitReplicates:

    def __init__(self):
        self.replicates = None
        self.column = None
        self.delimiter = None
        self.spliton = ' '
    
    def setOptions(self, opt):
        try: self.column = int(opt['column']) -1
        except KeyError: pass
        try: self.replicates = opt['replicates']
        except KeyError: pass
        try: self.delimiter = opt['delimiter']
        except KeyError: pass
        try: self.spliton = opt['spliton']
        except KeyError: pass
    
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
                #Replicate
                tmp.append('Replicate')
                name = row[self.column]
                list.append(tmp)
            else:
                # If the row is not empty
                if row != None and row != []:
                    # If the first element is not empty
                    if row[0] != None and row[0].strip() != '':
                        try:
                            tmp = row[0].strip().lower().split(self.spliton)
                            rep = tmp [(len(tmp)-1)]
                            row[0] = ''.join(tmp[:-1])
                            tmp = [el for el in row]
                            try:
                                tmp.append(self.replicates.index(rep) + 1)
                            except ValueError, err:
                                print "Error: Cant not find index of '%s' in %s. \n%s" %(rep, self.replicates, err)
                        except IndexError, err:
                            tmp = [el for el in row]
                        list.append(tmp)
        
        print " *** %d lignes has been read ***" %(lineNum)

        return list
