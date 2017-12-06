#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: cronner.py
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
__date__      = '17/04/2014'

import os
from subprocess import Popen, PIPE

class Cronner:
    def __init__(self):
        self.__minute = "0"
        self.__hour = "0"
        self.__month = "*"
        self.__dayOfMonth = "*"
        self.__dayOfWeek = "6"

    def addToCrontab(self):
        out, err = Popen("which python".split(), stdout=PIPE, stderr=PIPE).communicate()
        record = " ".join([self.__minute, self.__hour, self.__dayOfMonth, self.__month, self.__dayOfWeek, "root", "cd %s &&"%os.path.join(os.getcwd(), ("","libs")["libs" not in os.getcwd()]), out.strip(), os.path.join(os.getcwd(), ("","libs")["libs" not in os.getcwd()], "refreshPhoneBook.py")])+"\n"

        fpath = os.path.join(os.path.sep, "etc", "crontab")
        fp = open(fpath, "r")
        rd = fp.read()
        fp.close()

        if record not in rd:
            fp = open(fpath, "a")
            fp.write(record)
            fp.close()
    
    def getDayOfMonth(self):
        return __dayOfMonth
    
    def getDayOfWeek(self):
        return __dayOfWeek

    def getHour(self):
        return __hour

    def getMinute(self):
        return __minute

    def getMonth(self):
        return __month

    def setDayOfMonth(self, dayOfMonth):
        self.__dayOfMonth = dayOfMonth
    
    def setDayOfWeek(self, dayOfWeek):
        self.__dayOfWeek = dayOfWeek

    def setHour(self, hour):
        self.__hour = hour
 
    def setMinute(self, minute):
        self.__minute = minute

    def setMonth(self, month):
        self.__month = month

