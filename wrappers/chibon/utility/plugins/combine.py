#!/usr/bin/python
#-*- coding: UTF-8 -*-


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

import getopt, csv, sys

class combine:
        
    def main(self, readers):

        (reader, tocomb) = readers
        
        # Create the list of lines of the new csv files
        list = [] 
        header = []
        values = []
        
        # If the input file is not specified
        if not reader or not tocomb:
            sys.exit("\n***  Please define the input files  ***\n")

        # Read the file containing the values to combine
        lineNum = 0
        for row in tocomb:
            lineNum = lineNum + 1
            if lineNum == 1:
                header = row
            else:
                values = row

        lineNum = 0
        for row in reader: 
            # count the number of line in the file
            lineNum = lineNum + 1
            # Combine the two first row
            if lineNum == 1:
                [row.append(str(i)) for i in header]
                list.append(row)
            # First line contains the header -> Not to take into account
            if lineNum != 1: 
                # If the row is not empty
                if row != None and row != []:
                    # If the first element is not empty
                    if row[0] != None and row[0].strip() != '':
                        [row.append(str(i)) for i in values]
                        list.append(row)

        # Print a report of the work done
        print " *** %d lignes has been read ***" %lineNum 
        print " *** %d columns in the old file ***" %(len(row)-len(header))
        print " *** %d columns in the new file ***" %len(row)
        print " *** %d columns have been added ***" %len(header)

        return list

        return 0

