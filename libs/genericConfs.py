#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: genericConfs.py
# Copyright (c) 2014 by None
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
#
__author__    = 'Blasis Dimitriadis <blasisd@gmail.com>'
__docformat__ = 'plaintext'
__date__      = '08/04/2014'


class GenericConf:
    def __init__(self, confPath, delimiter = "=", commentChar = "#", punctuator = ""):
        "Initialized with the configuration file's path and assignment delimiter"
        self.__delimiter = delimiter
        self.__commentChar = commentChar
        self.__punctuator = punctuator
        self.__confPath = confPath
        self.__lines = self.readConfLines()
        self.__vars = {}

    def commit(self):
        fp = open(self.__confPath, "w")
        fp.writelines(self.__lines)
        fp.close()
              
    def getValue(self, varName):
        "Return var's value"
        contLine = "".join([line for line in self.__lines if varName+self.__delimiter in line.replace(" ","").replace("\t","") and not line.startswith(self.__commentChar)])
        varLines = ""
        if self.__punctuator and self.__punctuator not in contLine:
            for line in self.__lines[self.__lines.index(contLine):]:
                varLines += line
                if self.__punctuator in line:
                    break
        key,value = [[varName, ""], varLines.split(self.__delimiter, 1)][len(varLines)!=0]
        self.__vars[key.strip()] = contLine   # Now we know the exact line where this varName is found
        return value.strip().strip(self.__punctuator)

    def readConfLines(self):
        "Read configuration's file lines"
        fp = open(self.__confPath, "r")
        lines = fp.readlines()
        fp.close()
        return lines

    def setValue(self, varName, varValue):
        "Change a specific variable's value"
        self.getValue(varName)
        if type(varValue) == bool:
            varValue=str(varValue).upper()
        updatedLine = varName+self.__delimiter+str(varValue)+self.__punctuator
        if self.__vars[varName] not in self.__lines:
            for line in updatedLine.splitlines():
                self.__lines.append(line+"\n")
        else:
            multiLines = updatedLine.splitlines()
            indx = self.__lines.index(self.__vars[varName])
            for counter in xrange(0, len(multiLines)) :
                self.__lines[indx+counter] = multiLines[counter]+"\n"

    def uncomment(self, varNames = []):
        "Uncomment lines in conf file, that concern specific variables' assignments"
        for varName in varNames:
            for line in self.__lines:
                tmpLine = line
                if varName+self.__delimiter in tmpLine.replace(" ","").replace("\t","") and line.startswith(self.__commentChar):
                    self.__lines[self.__lines.index(line)]=line.strip(self.__commentChar)
                         
