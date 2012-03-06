#!/usr/bin/python
#-*- coding: UTF-8 -*-

# Handle database connection using sqlAchemy

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

from sqlalchemy import *
from sqlalchemy.databases import mysql
from sqlalchemy.orm import *
from sqlalchemy.sql import *

br = '<br />\n'

Tomato = {
    'dbName':'db_name',
    'dbUser':'user_name',
    'dbHost':'db_host',
    'dbPasswd':'db_pass',
    }

credential = {
    'Tomato':Tomato,
    }													     }


class DBConnection:
    '''
    Class that handles the connection to the databast through the sqlAchemy layer
    which is an equivalent in python of the persistant layer used in Java.
    
    It links all the class of the database to an object in python.
    '''
    
    def __init__(self, dbName):
        print dbName
        cred = credential[dbName]
        self.dbName = cred['dbName']    
        self.dbUser = cred['dbUser']
        self.dbPasswd = cred['dbPasswd']
        self.dbHost = cred['dbHost']
        self.con = create_engine('mysql://%s:%s@%s/%s'%(self.dbUser, self.dbPasswd, self.dbHost, self.dbName), encoding='utf-8', convert_unicode=True)
        self.con.echo = False
        self.metadata = MetaData(self.con)

        self.genotype = Table('pp_genotype', self.metadata, autoload = True)
        self.exp_design = Table('ph_exp_design', self.metadata, autoload = True)
        self.observation = Table('ph_observation', self.metadata, autoload = True)
        self.map_info = Table('ma_maps_info', self.metadata, autoload = True)
        self.maps = Table('ma_maps', self.metadata, autoload = True)
        
        self.genomapper = mapper(Genotype, self.genotype)
        self.designmapper = mapper(Exp_design, self.exp_design)
        self.observationmapper = mapper(Observation, self.observation)
        self.map_infomapper = mapper(MapInfo, self.map_info)
        self.mapsmapper = mapper(Maps, self.maps)

        self.session = create_session()
        
    def hasGeno(self, id):
        ''' Check if a given genoID is present in the database '''
        g = self.session.query(Genotype).filter(self.genotype.c.genoID == id)
        if not g or g.count() == 0: 
            return None
        elif g.count() !=  1:
            return False
        else:
            return g[0].genoID
    
    def hasDesign(self, mb_nr):
        ''' Check if a given mb_nr is present in the database '''
        e = self.session.query(Exp_design).filter(self.exp_design.c.mb_nr == mb_nr)
        if not e or e.count() == 0: 
            return None
        elif e.count() !=  1:
            return False
        else:
            return e[0].mb_nr
    
    def hasObs(self, mb_nr, trtid, rep, date, sub_divide):
        ''' Check if a given observation (with the experiment info) is in the database '''
        p = self.session.query(Observation).filter(and_(self.observation.c.mb_nr == mb_nr, \
                                                        self.observation.c.trtID == trtid, \
                                                        self.observation.c.replicate == rep, \
                                                        self.observation.c.date == date, \
                                                        self.observation.c.sub_divide == sub_divide))
        if not p or p.count() == 0: 
            return None
        elif p.count() !=  1:
            return False
        else:
            return p[0].mb_nr
    
    def hasMapInfo(self, mapinfo):
        ''' Check if a given map has info in the database '''
        #print mapinfo
        p = self.session.query(MapInfo).filter(and_(
                                                    self.map_info.c.mapDescription == mapinfo['mapDescription'], \
                                                    self.map_info.c.mapType == mapinfo['mapType'], \
                                                    self.map_info.c.mapSoftware == mapinfo['mapSoftware'], \
                                                    self.map_info.c.calculatedBy == mapinfo['calculatedBy'], \
                                                    self.map_info.c.addr == mapinfo['addr'], \
                                                    )
                                                )
        if not p or p.count() == 0:
            return None
        elif p.count() > 1:
            return False
        else:
            return p[0].mapID
    
    def hasMap(self, map):
        ''' Check if a given map is present in the ma_maps of the database '''
        #print map
        p = self.session.query(Maps).filter(and_(
                                                    self.maps.c.mapID == map['mapID'], \
                                                    self.maps.c.markerName == map['markerName'], \
                                                    )
                                                )
        if not p or p.count() == 0:
            return None
        elif p.count() > 1:
            return False
        else:
            return True

class Genotype(object):
    pass

class Exp_design(object):
    pass

class Observation(object):
    pass

class MapInfo(object):
    pass

class Maps (object):
    pass

