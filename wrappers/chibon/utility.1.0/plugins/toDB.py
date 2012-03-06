#!/usr/bin/python
#-*- coding: UTF-8 -*-

#*****************************************************
# toDB.py
#
# This script take a list of queries and execute them
#
#
# Made the 26th February 2009
# by Pierre-Yves chibon
#
# Version 1.0 - 26th January 2008
#   * Run the queries
#
#*****************************************************
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

import getopt, csv, sys, MySQLdb
from types import *
sys.path.append('..')
from Database import Database
from optparse import OptionParser

USAGE ="""
This program takes a .sql file as input
Please use --help to see the options available.
"""


#***********************************************************************
### argument
# retrieve the arguments given and show the help when needed
def getArgument():
    # Handle the parameters
    parser = OptionParser(version="%prog 1.0")
    parser.add_option("-f", "--file", dest="inputFile", type="string",
                  help="The input file (text file with the value separated by a semi-colon';').")
    parser.add_option("-d", "--database", dest="database", default='localPotato', type="string",
                  help="The database configuration to use.")

    (options, args) = parser.parse_args()

    return (options.inputFile, options.database)
#***********************************************************************


class toDB:
    
    def __init__(self):
        pass
    
    def setOptions(self, opt):
        try:
            self.database = opt['database']
        except KeyError, err:
            pass
    
    ### main
    # Do the job :)
    def main(self, reader):
        
        self.db = Database(self.database)
        self.db.VERBOSE = False
        
        self.db.DBconnection()

        lineNum = 0
        failed = []
        passed = 0
        for row in reader: 
            lineNum = lineNum + 1
            r = self.db.runInsert(row)
            if r is None:
                failed.append(row)
            else:
                passed = passed +1
        
        self.db.DBclose()
        
        # Print a report of the work done
        print " *** %d queries has been performed ***" %lineNum 
        print " *** %s queries have failed ***" %len(failed)
        print " *** %s queries have passed ***" %passed
        
        print "\n","\n".join(failed)

        return 0

if __name__ == '__main__': 
    # Retrieve the given arguments
    (inputFile, database) = getArgument()

    # If the input file is not specified
    if not inputFile: 
        sys.exit("\n***  Please define the input files  ***\n" +  USAGE)
    if not inputFile.endswith('.sql'):
        sys.exit("\n***  Wrong type of input file  ***\n" +  USAGE)
    
    reader = open(inputFile, "rb")
    obj = toDB()
    obj.database = database
    obj.main(reader)
