#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: faxClientsGenerator.py
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

class FaxClientsGenerator:
    def __init__(self):
        self.__startIP = "192.168.1.1"
        self.__endIP = "192.168.1.254"
        self.__extraIPs = []

    def getFaxClientsIPs(self):
        "Return fax clients' IPs, in order to add them to elastix's 'allowance' list. For now, we assume that all ips have the same subnetID"     
        subnetID, limitStart = os.path.splitext(self.__startIP)
        limitEnd = os.path.splitext(self.__endIP)[-1] 
            
        ipsLst = [subnetID+"."+str(i) for i in xrange(int(limitStart.strip(".")), int(limitEnd.strip("."))+1)]+self.__extraIPs
        return ipsLst

    def setStartIP(self, startIP):
        self.__startIP = startIP

    def setEndIP(self, endIP):
        self.__endIP = endIP
        
    def setExtraIPs(self, extraIPs):
        self.__extraIPs = extraIPs

