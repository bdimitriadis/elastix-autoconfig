#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: ldapper.py
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
__date__      = '16/04/2014'

try:
    import ldap
except ImportError:
    from subprocess import Popen, PIPE
    "Install python-ldap, if it is not already installed"
    pf = Popen("cat /etc/issue".split(), stdout=PIPE, stderr=PIPE)
    output = pf.communicate()
    if output[1]:
       print output[1]
    else:
        if "CentOS" in output[0]:
            installer="yum"
        elif "Ubuntu" in output[0] or "Debian" in output[0]:
            installer="apt-get"
        else:
            print "Cannot install python-ldap on this linux distribution. Sorry!"   
            sys.exit()

    pf = Popen((installer+" install -y python-ldap").split(), stdout=PIPE, stderr=PIPE)
    output = pf.communicate()
    if output[1]:
        print output[1]
    else:
        print output[0]
    import ldap


class Ldapper:
    """Class used for retrieving users' info from an ldap server."""
    def __init__(self, aimsServer = "", baseDn = ""):
        self.__aimsServer = aimsServer
        self.__baseDn = baseDn
        self.__retrAttrs = ""

    def getBaseDn(self):
        return self.__baseDn

    def getHost(self):
        return self.__aimsServer

    def ldapRead(self, retrAttrs=["cn", "givenName", "sn", "telephoneNumber", "ou", "mail", "postOfficeBox"]):
        "Return a list of all the dics containing the users' information we need (first and lastname and phone)"
        directory = ldap.open(self.__aimsServer)
        directory.simple_bind_s()

        if not self.__retrAttrs:
            self.__retrAttrs = map(str, retrAttrs)
        results = directory.search_s(self.__baseDn, ldap.SCOPE_SUBTREE, attrlist = self.__retrAttrs)

        dics = [res[1] for res in results if res!=results[0]]

        return dics 

    def setBaseDn(self, baseDn):
        self.__baseDn = baseDn

    def setHost(self, host):
        self.__aimsServer = host

    def setRetrAttrs(self, retrAttrs):
        self.__retrAttrs = map(str, retrAttrs)
