#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: postfixConfs.py
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
__date__      = '27/03/2014'

from subprocess import Popen, PIPE
import os, sys
from genericConfs import GenericConf
import getpass

class PostfixConfs:

    def __init__(self):
        self.__postfixServicePath = os.path.join(os.path.sep,"etc","init.d","postfix")
        self.__confFilename = os.path.join(os.path.sep,"etc","postfix", "main.cf")
       
        if not os.path.isfile(self.__postfixServicePath) or not os.path.exists(os.path.join(os.path.sep, "etc","postfix")):
            print "Exiting: Most probably postfix is not yet installed on your system."
            sys.exit(1)
        self.postfixObj = GenericConf(self.__confFilename, "=")
        self.postFixVars={}

    def commit(self):
        self.postfixObj.commit()

    def getAuthEnable(self):
        return self.postfixObj.getValue("smtp_sasl_auth_enable")
        
    def getMessageSizeLimit(self):
        return self.postfixObj.getValue("message_size_limit")

    def getMyOrigin(self):
        return self.postfixObj.getValue("myorigin")

    def getRelayDomains(self):
        return self.postfixObj.getValue("relay_domains")

    def getRelayHost(self):
        return self.postfixObj.getValue("relayhost")

    def getPasswordMaps(self):
        return self.postfixObj.getValue("smtp_sasl_password_maps")

    def getSecurityOptions(self):
        return self.postfixObj.getValue("smtp_sasl_security_options")
       
    def setAuthEnable(self, authEnableVal = "yes"):
        "Enable or disable authentication"
        self.postfixObj.setValue("smtp_sasl_auth_enable", authEnableVal)
       
    def setMessageSizeLimit(self, size=102400000):
        "Define message's max size limit"
        self.postfixObj.setValue("message_size_limit", size)

    def setMyOrigin(self, myoriginVal = "$myhostname"):
        "Specify the domain that locally-posted mail appears to come from"
        self.postfixObj.setValue("myorigin", myoriginVal)
 
    def setPasswordMaps(self, passwordMapsVal = "hash:/etc/postfix/password"):
        "Set password maps"
        self.postfixObj.setValue("smtp_sasl_password_maps", passwordMapsVal)

    def setRelayDomains(self, relayDomVal = "$mydestination"):
        "Restrict what destinations this system will relay mail to"
        self.postfixObj.setValue("relay_domains", relayDomVal)

    def setRelayHost(self, relayhostVal = "$mydomain"):
        "Specify the default host to send mail to when no entry is matched in the optional transport table"
        self.postfixObj.setValue("relayhost", relayhostVal)
 
    def setSecurityOptions(self, securityOptionsVal = ""):
        "Set security options"
        self.postfixObj.setValue("smtp_sasl_security_options", securityOptionsVal)

    def setSmtpAddr(self, smtpAddr, userName=None, password=None):
        while not userName:
            userName = raw_input("Please enter smtp username:")
        while not password:
            pprompt = lambda: (getpass.getpass("Please enter smtp password:"), getpass.getpass('Retype password for verification: '))
            p1, p2 = pprompt()
            while p1 != p2:
                print 'Passwords do not match. Try again'
                p1, p2 = pprompt()
            password = p1

        headPath = os.path.dirname(self.__confFilename)
        fp=open(os.path.join(headPath,"password"), "w")
        fp.write(smtpAddr+" "+userName+":"+password)
        fp.close()

        oldCwd = os.getcwd()
        os.chdir(headPath)
        pf = Popen("postmap password".split(), stdout=PIPE, stderr=PIPE)
        output = pf.communicate()
        if output[1]:
            print output[1]
        else:
            print output[0]
            pf = Popen("chmod 600 password password.db".split(), stdout=PIPE, stderr=PIPE)
            output = pf.communicate()
            if output[1]:
                print output[1]
            else:
                print output[0]
            
            os.unlink("password")
            os.chdir(oldCwd)
        
        

        

        
