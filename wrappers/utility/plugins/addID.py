#!/usr/bin/python
#-*- coding: UTF-8 -*-

# Add an extra-field called ID and fill it with the line number

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

class addID:
    
    def getLineNum(self, num):
        x = 5
        n = len(str(num -1))
        return "0"*(x-n) + str(num-1)

    def main(self, reader):
        
        genoList = []        

        # If the input file is not specified
        if not reader:
            sys.exit("\n***  Please define one input file  ***\n")

        lineNum = 0
        for row in reader: 
            # count the number of line in the file
            lineNum = lineNum + 1
            if lineNum == 1:
                tmp = [el for el in row]
                tmp.append('ID')
                genoList.append(tmp)
            else:
                tmp = [el for el in row]
                tmp.append(self.getLineNum(lineNum))
                genoList.append(tmp)
            

        # Print a report of the work done
        print " *** %d lignes has been read ***" %lineNum 
        
        return genoList
