#!/usr/bin/python
#-*- coding: UTF-8 -*-

# For each rows in the reader 
## Check if the genotype is already present in the database
## Check if the genotypes already has a entry in ph_exp_design
## Check if the genotypes has already for this position in the experiment an observation
## Generate the correct query
# Write the file of queries

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
from DBConnection import DBConnection

list = []
nogood = []

class CxE02generateQueries:

    def __init__(self):
        self.database = None
        self.delimiter = None
        self.session = None
        self.debug = False
    
    def setOptions(self, opt):
        try: self.database = opt['database']
        except KeyError: pass
        try: self.debug = int(opt['debug'])
        except KeyError: pass
        try: self.delimiter = opt['delimiter']
        except KeyError: pass
        
    
    
    def main(self, reader):
        
        # If the input file is not specified
        if not reader:
            sys.exit("\n***  Please define one input file  ***\n")
        
        db = DBConnection(self.database)
    
        genoabs = []
        genodouble = []
        
        obspresent = []
        obsdouble = []
        
        designpresent = []
        designdouble = []
        
        queries = []
        
        lineNum = 0
        name = None
        for row in reader: 
            # count the number of line in the file
            lineNum = lineNum + 1
            # First line contains the header -> Direct to the output
            if lineNum == 1:
                header = [el.lower() for el in row]
            else:
                # If the row is not empty
                if row != None and row != []:
                    # If the first element is not empty
                    if row[0] != None and row[0].strip() != '':
                        
                        ## Check if the genotype is present
                        genoid = row[header.index('genoid')]
                        g = db.hasGeno(genoid)
                        
                        if g is None:
                            if genoid not in genoabs: genoabs.append(genoid)
                            if self.debug: print "* The genotype with the genoID : '%s' is not present in the database" %(genoid)
                        elif g is False:
                            if genoid not in genodouble: genodouble.append(genoid)
                            if self.debug: print "* Several genotypes with the genoID : '%s' have been found in the database" %(genoid)
                        else:
                            
                            ## Check if the present genotype are already in the design
                            mb_nr = row[header.index('expid')] + row[header.index('year')] + row[header.index('id')]
                            d = db.hasDesign(mb_nr)
                            
                            if d is not None:
                                if mb_nr not in designpresent: designpresent.append(mb_nr)
                                if self.debug: print "* The exp_design with the mb_nr : '%s' is already present in the database" %(mb_nr)
                            elif d is False:
                                if mb_nr not in designdouble: designdouble.append(mb_nr)
                                if self.debug: print "* Several exp_design with the mb_nr : '%s' have been found in the database" %(mb_nr)
                            else:
                                query = "INSERT INTO ph_exp_design (mb_nr, genoID, expID, DateCreated) \
 VALUES ('%s', '%s', '%s', CURDATE());" %(mb_nr, genoid, row[header.index('expid')])
                                
                                queries.append(query)
                                
                            ## Check if they have an observation
                            obs =  row[header.index('obs')]
                            trtid = row[header.index('trtid')]
                            rep = row[header.index('replicate')]
                            methid = row[header.index('methid')]
                            date = row[header.index('date')]
                            try: sub_divide = row[header.index('sub_divide')]
                            except Exception, err: sub_divide = 1
                            
                            o = db.hasObs(mb_nr, trtid, rep, date, sub_divide)
                            
                            if o is not None:
                                if mb_nr not in obspresent: obspresent.append(mb_nr)
                                if self.debug: print "* The observation with the mb_nr : '%s' is already present in the database" %(mb_nr)
                            elif d is False:
                                if mb_nr not in obspresent: obsdouble.append(mb_nr)
                                if self.debug: print "* Several observation with the mb_nr : '%s' have been found in the database" %(mb_nr)    
                            else:
                                query = "INSERT INTO ph_observation (mb_nr, trtID, replicate, date, sub_divide, methID, t_score, n_score, DateCreated) \
 VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', CURDATE());" %(mb_nr, trtid, rep, date, sub_divide, methid, obs, obs)
                                
                                queries.append(query)
        
        print " *** %d lignes has been read (included one header)***\n" %(lineNum)
        print " *** %d geno are not present in the database *** " %(len(genoabs))
        if self.debug: print genoabs
        print " *** %d geno are present more than one time in the database *** " %(len(genodouble))
        if self.debug: print genodouble
        print " *** %d design were already present  in the database *** " %(len(designpresent))
        if self.debug: print designpresent
        print " *** %d design are present more than one time in the database *** " %(len(designdouble))
        if self.debug: print designdouble
        print " *** %d observations were already present  in the database *** " %(len(obspresent))
        if self.debug: print obspresent
        print " *** %d observations are present more than one time in the database *** " %(len(obsdouble))
        if self.debug: print obsdouble
        

        return queries
