#-*- coding: UTF-8 -*-

"""
This file handles the read and access of the configuration file given.

(c) Copyright Pierre-Yves Chibon -- 2009-2012

Distributed under License GPLv3 or later
You can find a copy of this license on the website
http://www.gnu.org/licenses/gpl.html

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
   
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
   
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""

import os, sys
from ConfigParser import ConfigParser


class ConfError(Exception):
    """ Basic exception class to be used for the configuration error.
    """
    pass


class Conf:
    """ Handles the configuration file for the pipeline using
    ConfigParser.
    """

    def __init__(self, conffile=None):
        """ Constructor, loads the configuration.
        :kwarg conffile, the full path to the configuration file for the
        pipeline.
        """
        self.conffile = conffile
        self.config = ConfigParser()
        self.config.readfp(open(conffile))
       
    def getModules(self, conffile=None):
        """ Return a list of Modules to set in the configuration file
        :kwarg conffile, the full path to the configuration file for the
        pipeline, if None, use the configuration file set in the
        constructor.
        """
        if not conffile:
            conffile = self.conffile
        if not conffile:
            raise ConfError('No configuration file specified')
        mod = {}
        i = 1
        while self.config.has_option('Modules', str(i)):
            try:
                mod[i] = self.config.get('Modules', str(i))
            except ConfigParser.NoOptionError, err:
                raise ConfError('The configuration file "%s" does not '\
                'have the option "%s"' % (conffile, i))
            i = i + 1
        return mod
        
    def getSection(self, section):
        """ Return the dictionnary of the content of the asked section
        from the configuration file.
        :arg section, name of the section to return.
        """
        mod = {}
        i = 1
        for opt in self.config.options(section):
            mod[opt] = self.config.get(section, opt)
            i = i + 1
        return mod
    
    def getOptions(self, section):
        """ Return the options for the asked section.
        :arg section, name of the section to return.
        """
        return self.config.options(section)
