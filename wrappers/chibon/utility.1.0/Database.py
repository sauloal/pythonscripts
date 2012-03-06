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

import sys, MySQLdb


Tomato = {
    'dbName':'db_name',
    'dbUser':'user_name',
    'dbHost':'db_host',
    'dbPasswd':'db_pass',
    }

credential = {
    'Tomato':Tomato,
    }

class Database:
    '''
        Creates the database class and gives it the connection information
    '''
    def __init__(self, dbName):
        print dbName
        cred = credential[dbName]
        ''' Instanciate the object with the default value for the database '''
        self.dbName = cred['dbName']    
        self.dbUser = cred['dbUser']
        self.dbPasswd = cred['dbPasswd']
        self.dbHost = cred['dbHost']
        self.con = None
        self.VERBOSE = True
        
    def DBconnection(self):
        ''' Set up the connection to the database '''
        self.con = MySQLdb.connect(host = self.dbHost, user = self.dbUser , passwd = self.dbPasswd, db = self.dbName)
        
    def DBclose(self):
        ''' Close the connection to the database'''
        self.con.close()

    def runSelectAll(self, query):
      try:
          self.cursor = self.con.cursor()
          result = self.cursor.execute(query)
          result_set = self.cursor.fetchall ()
          results = []
          for row in result_set:
                results.append(str(row[0]))
          self.cursor.close()
          self.con.commit()
          return True
      except Exception, err:
          if self.VERBOSE: print "\nQUERY FAILED !!\n %s \n %s" %(query, err)
          return None
      return results
      
    def runInsert(self, query):
      try:
          self.cursor = self.con.cursor()
          self.cursor.execute(query)
          self.cursor.close()
          self.con.commit()
          return True
      except Exception, err:
          if self.VERBOSE: print "\nQUERY FAILED !!\n %s \n %s" %(query, err)
          return None
          
    def runSelect(self, query):
      try:
          self.cursor = self.con.cursor()
          result = self.cursor.execute(query)
          result = self.cursor.fetchone()
          self.cursor.close()
          self.con.commit()
          return result
      except Exception, err:
          if self.VERBOSE: print "\nQUERY FAILED !!\n %s \n %s" %(query, err)
          return None
