#!/usr/bin/python
#-*- coding: UTF-8 -*-


#*****************************************************
# addCE
#
# This script add CE to the list of genotype name given
#
#
# Made the 20th January 2009
# by Pierre-Yves chibon
#
# Version 1.4 - 24th February 2009
#   * Handle control genotypes
# Version 1.3 - 24th February 2009
#   * Only change numbers
# Version 1.2 - 17th February 2009
#   * Uses the writeFile method
# Version 1.1 - 17th February 2009
#   * Handle the C and E
# Version 1.0 - 20th January 2009
#   * Add CE
#
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
#*******************************************************************************
# Create the different lists used to insert/update the data in the database in 
# the correct order after

class addCE:
    
    def __init__(self):
        self.addID = False
        self.column = None
    
    def setOptions(self, opt):
        try: self.addID = opt['addid']
        except KeyError: pass
        try: self.column = int(opt['column']) -1
        except KeyError: pass

    def getID(self, name):
        name = name.replace('-','')
        name = name.replace(' ','')
        if len(name.lower().split('ce')) > 1:
            tmp = name.lower().split('ce')[1]
            try:
                int(tmp)
            except Exception, err:
                print '*** %s \n *%s' %(tmp, err)
                #int(tmp)
            s = 10 - len(tmp) - 2
            return 'CE' + '0'*s + tmp
        if len(name) >= 10:
            return name.upper()[:9] + '1'
        else:
            s = 10 - len(name) - 1
            return name.upper() + '0'*s + '1'

    def main(self, reader):
        
        genoList = []
        

        # If the input file is not specified
        if not reader:
            sys.exit("\n***  Please define one input file  ***\n")

        lineNum = 0
        for row in reader: 
            # count the number of line in the file
            lineNum = lineNum + 1
            # If the row is not empty
            if row != None and row != []:
                # If the first element is not empty
                if row[0] != None and row[0].strip() != '':
                    # change the column given to add the CE code
                    if lineNum == 1:
                      if self.addID:
                        row.append('GenoID')
                      genoList.append(row)
                    else:
                      name = row[self.column]
                      try:
                          int(name)
                          if len(name) == 2:
                            name = '0' +  name
                          name = 'CE' +  name
                          row[self.column] = name
                      except ValueError, err:
                        pass
                      if self.addID:
                        row.append(self.getID(name))
                      genoList.append(row)

        # Print a report of the work done
        print " *** %d lignes has been read ***" %lineNum 
        
        return genoList
