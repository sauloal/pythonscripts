#!/usr/bin/python
#-*- coding: UTF-8 -*-

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

import os, csv

VERBOSE = False
#VERBOSE = True

class compare:
       
    def main(self, file1, file2):
        
        if len(file1) < len(file2):
            maxlen = len(file1)
            print "The two files don't have the same length (%s - %s) !" %(len(file1), len(file2))
        elif len(file1) > len(file2):
            maxlen = len(file2)
            print "The two files don't have the same length (%s - %s) !" %(len(file1), len(file2))
        else:
            maxlen = len(file1)
            print "The two files have the same length (%s) !" %(maxlen)
        
        print "(row,col)"
        print "File1 (%s, %s)" %(len(file1), len(file1[0]))
        print "File2 (%s, %s)" %(len(file2), len(file2[0]))
        #maxlen = 2
        notok = []
        colchange = []
        ok = 0
        rowcnt = 0
        while rowcnt < maxlen:
            if file1[rowcnt] != file2[rowcnt]:
                notok.append(rowcnt)
                colcnt = 0
                #print file1[rowcnt], '--', file2[rowcnt]
                while colcnt < len(file1[rowcnt]) :# and colcnt < 3:
                    if file1[rowcnt][colcnt] != file2[rowcnt][colcnt] and VERBOSE:
                        print "(%s,%s) 1- '%s'    2- '%s'" %(rowcnt, colcnt, file1[rowcnt][colcnt], file2[rowcnt][colcnt])
                        if colcnt not in colchange:
                            colchange.append(colcnt)
                        
                    colcnt = colcnt + 1
                #if VERBOSE: print " 1- %s \n 2- %s" %(file1[rowcnt], file2[rowcnt])
            else: ok = ok + 1
            rowcnt = rowcnt + 1
        
        print " *** %s rows are identical ***" %ok
        print " *** %s rows are *not* identical ***" %(len(notok))
        print " *** %s columns are *not* identical ***" %(len(colchange))
        if VERBOSE:
            print notok
            print colchange


if __name__ == "__main__":
    
    #file1 = '/home/pierrey/Desktop/FreqDist/All_peak2-out-Peel-avg2.csv'
    #file2 = '/home/pierrey/Desktop/FreqDist/All_peak2-out-Peel-avg.csv'
    
    #file1 = '/home/pierrey/Desktop/FreqDist/peel_metabolite-complete4000-out-avg2.csv'
    #file2 = '/home/pierrey/Desktop/FreqDist/peel_metabolite-complete4000-out-avg3.csv'
    
    #file1 = '/home/pierrey/Desktop/Data_Mod3/Run1c/Map-out.csv'
    #file2 = '/home/pierrey/Desktop/Data_Mod3/Run1c/Genotypes-out-ordered.csv'
    #file1 = '/home/pierrey/Desktop/Data_Mod3/Run2c/Map-out.csv'
    #file2 = '/home/pierrey/Desktop/Data_Mod3/Run2c/Genotypes-out-ordered.csv'
    #file1 = '/home/pierrey/Desktop/Data_Mod3/Run3/Map-out.csv'
    #file2 = '/home/pierrey/Desktop/Data_Mod3/Run3/Genotypes-out-out.csv'
    #file1 = '/home/pierrey/Desktop/Data_Mod3/Run4/Map-out.csv'
    #file2 = '/home/pierrey/Desktop/Data_Mod3/Run4/Genotypes-out-out.csv'
    
    #file1 = '/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod3/Run1c/Genotypes-out-out-ordered.csv'
    #file2 = '/home/pierrey/Desktop/Data_Mod4/Run1c/Genotypes-out-ordered-out.csv'
    
    #file1 = '/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod3/Run1c/Genotypes-out.csv'
    #file2 = '/home/pierrey/Desktop/Data_Mod4/Run1c/Genotypes-out.csv'
    
    #file1 = '/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod3/Run1c/MetaNetwork/qtlSumm.csv'
    #file2 = '/home/pierrey/Desktop/Data_Mod4/Run1c/MetaNetwork/qtlSumm.csv'
    
    #file1 = '/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod3/Run1c/MetaNetwork/qtlProfiles.csv'
    #file2 = '/home/pierrey/Desktop/Data_Mod4/Run1c/MetaNetwork/qtlProfiles.csv'
    
    #file1 = '/home/pierrey/Desktop/Data_Mod4/Run4b/Genotypes-out-out-ordered.csv'
    #file2 = '/home/pierrey/Desktop/Data_Mod4/Run3b/Genotypes-out-out-ordered.csv'
    
    #file1 = "/var/www/html/Bjorn/PY-CxE-MN-runs-2010/Cy3-C-0--1/MetaNetwork/qtlProfiles.csv"
    #file2 = "/var/www/html/Bjorn/PY-CxE-MN-runs-2010/Cy3-C-0/MetaNetwork/qtlProfiles.csv"
    
    #file1 = "/var/www/html/Bjorn/PY-CxE-MN-runs-2010/Cy3-C-0--1/MetaNetwork/qtlSumm.csv"
    #file2 = "/var/www/html/Bjorn/PY-CxE-MN-runs-2010/Cy3-C-0/MetaNetwork/qtlSumm.csv"
    #file1 = "/var/www/html/Bjorn/yarp-test/EasyRqtl_crossObject.csv"
    #file2 = "/var/www/html/Bjorn/yarp-test/EasyRqtl_crossObject1.csv"
    file1 = "/var/www/html/Bjorn/yarp-test/EasyRqtl_ndraw100-4_qtlSummary_bayesian.csv"
    file2 = "/var/www/html/Bjorn/yarp-test/EasyRqtl_ndraw100-3_qtlSummary_bayesian.csv"
    
    reader1 = csv.reader(open(file1, "rb"), delimiter = ',')
    reader2 = csv.reader(open(file2, "rb"), delimiter = ',')
    
    reader1 = [row for row in reader1]
    reader2 = [row for row in reader2]
    
    #reader1 = [row[0] for row in reader1]
    #reader2 = [row[0] for row in reader2]
    
    c = compare()
    c.main(reader1, reader2)





####################################################################################################
####################################################################################################
####################################################################################################

    ######## RUN 1
    #file1 = "/home/pierrey/Desktop/run1/Inputs/tic_metabolites--PeakList400-tbp-NA.csv"
    #file2 = "/home/pierrey/Desktop/Data_lp/Run1b/Metabolites-out.csv"
    # -> identical
    
    #file1 = "/home/pierrey/Desktop/run1/Inputs/Markers-3-4.csv"
    #file2 = "/home/pierrey/Desktop/Data_lp/Run1b/Map-out.csv"
    # headers and 2 lines inverted
    
    #file1 = "/home/pierrey/Desktop/run1/Inputs/Genotypes-4-3.csv"
    #file2 = "/home/pierrey/Desktop/Data_lp/Run1b/Genotypes-out2.csv"
    # Once sorted by name -> identical
    
    ######## RUN 2
    #file1 = "/home/pierrey/Desktop/run2/tic_flesh_apple.csv"
    #file2 = "/home/pierrey/Desktop/Run2b/Metabolites-out.csv"
    # -> identical
    
    #file1 = "/home/pierrey/Desktop/run2/Markers-3-4.csv"
    #file2 = "/home/pierrey/Desktop/Run2b/Map-out.csv"
    # headers and 2 lines inverted (once removed the I in the 3rd column)
    
    #file1 = "/home/pierrey/Desktop/run2/Genotypes-4-3.csv"
    #file2 = "/home/pierrey/Desktop/Run2b/Genotypes-out2.csv"
    # Once sorted by column and rows -> identical

####################################################################################################

    
    ####### RUN 1-2
    #file1 = "/home/pierrey/Desktop/Data_Mod2/Run1c/Metabolites-out.csv"
    #file2 = "/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod/Run1c/Metabolites-out.csv"
    # -> Identical
    
    #file1 = "/home/pierrey/Desktop/Data_Mod2/Run1c/Map-out.csv"
    #file2 = "/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod/Run1c/Map-out.csv"
    # -> Identical
    
    #file1 = "/home/pierrey/Desktop/Data_Mod2/Run1c/Genotypes-out.csv"
    #file2 = "/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod/Run1c/Genotypes-out.csv"
    # Once sorted by column -> Identical

    ####### RUN 2-2
    #file1 = "/home/pierrey/Desktop/Data_Mod2/Run2c/Metabolites-out.csv"
    #file2 = "/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod/Run2c/Metabolites-out.csv"
    # -> Identical
    
    #file1 = "/home/pierrey/Desktop/Data_Mod2/Run2c/Map-out.csv"
    #file2 = "/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod/Run2c/Map-out.csv"
    # -> Identical
    
    #file1 = "/home/pierrey/Desktop/Data_Mod2/Run2c/Genotypes-out.csv"
    #file2 = "/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod/Run2c/Genotypes-out.csv"
    # Once sorted by column -> Identical

    ####### RUN 3-2
    #file1 = "/home/pierrey/Desktop/Data_Mod2/Run3/Metabolites-out.csv"
    #file2 = "/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod/Run3/Metabolites-out.csv"
    # -> Identical
    
    #file1 = "/home/pierrey/Desktop/Data_Mod2/Run3/Map-out.csv"
    #file2 = "/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod/Run3/Map-out.csv"
    # -> Identical # I had to change the top line
    
    #file1 = "/home/pierrey/Desktop/Data_Mod2/Run3/Genotypes-out.csv"
    #file2 = "/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod/Run3/Genotypes-out.csv"
    # 2 markers have been added (I had to insert 2 blank lines to see the file are egual)

    ######## RUN 4-2
    #file1 = "/home/pierrey/Desktop/Data_Mod2/Run4/Metabolites-out.csv"
    #file2 = "/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod/Run4/Metabolites-out.csv"
    # -> Identical
    
    #file1 = "/home/pierrey/Desktop/Data_Mod2/Run4/Map-out.csv"
    #file2 = "/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod/Run4/Map-out.csv"
    # -> Identical # I had to change the top line
    
    #file1 = "/home/pierrey/Desktop/Data_Mod2/Run4/Genotypes-out.csv"
    #file2 = "/home/pierrey/Desktop/PRI_potato2/MetaNetwork/Ali/Runs/Data_Mod/Run4/Genotypes-out.csv"
    # 2 markers have been added (I had to insert 2 blank lines to see the file are egual)
    
