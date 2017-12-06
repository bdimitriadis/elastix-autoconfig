#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: elastixConfs.py
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
__date__      = '07/04/2014'


from postfixConfs import PostfixConfs
from httpdConfs import HttpdConfs
from asteriskConfs import AsteriskConfs
from ldapper import Ldapper
from phonebookCreator import PhoneBook
from cronner import Cronner
from faxClientsGenerator import FaxClientsGenerator
import os, sys
from subprocess import call as subcall, Popen, PIPE


try:
    import json
except ImportError:
    try:
        import simplejson as json
    except:
        "Install simplejson, if it is not already installed"
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
                print "Cannot install python-simplejson on this linux distribution. Sorry!"   
                sys.exit

        pf = Popen((installer+" install -y python-simplejson").split(), stdout=PIPE, stderr=PIPE)
        output = pf.communicate()
        if output[1]:
           print output[1]
        else:
           print output[0]
        import simplejson as json

class ElastixConfs:
    """Main class, consisting of objects coresponding to the various services used and functionalities needed by elastix. 
    Additional modules are implemented for setting, getting each objects' status, extracting a phonebook from an ldap server
    and generating faxclient IPs"""
    def __init__(self):
        fp = open(os.path.join(os.path.split(os.getcwd()+("/","")["libs" in os.getcwd()])[0],"conf","elastix.json"),"r")
        reload(sys)
        sys.setdefaultencoding("utf8")
        self.__confVars = json.loads(fp.read())
        fp.close()
        self.__servicesPath = os.path.join(os.path.sep, "etc", "init.d")
        self.__failsafe = ""
        if 'postfix' in self.__confVars.keys():
            self.postfixObj = PostfixConfs()
        if 'httpd' in self.__confVars.keys():
            self.httpdObj = HttpdConfs()
        if 'asterisk' in self.__confVars.keys():
            self.asteriskObj = AsteriskConfs()
        if 'ldap' in self.__confVars.keys():
            self.ldapObj = Ldapper()
        if 'cron' in self.__confVars.keys():
            self.cronObj = Cronner()
        if 'faxClients' in self.__confVars.keys():
            self.faxClientsObj = FaxClientsGenerator()
        self.phonebookObj = PhoneBook()
        self.__installNano()
        
    def __installNano(self):
        "Install nano editor, if it not already installed"
        if Popen("which nano".split(),stdout=PIPE, stderr=PIPE).communicate()[1]:
            pf = Popen("yum install -y nano".split(), stdout=PIPE, stderr=PIPE)
            output = pf.communicate()
            if output[1]:
                print output[1]
            else:
                print output[0]

    def fixAllConfs(self):
        "Set all atributes needed for all conf objects and extract all files needed"
        for serv in self.__confVars.keys():
            if serv == "elastix":
                continue
            self.setObj(serv)
            
            try:
                "Catch exception in case object in confVars.keys() does not have a commit member or does not refer to a service"
                exec "self."+serv+"Obj.commit()"
            except AttributeError:
                pass
            
            try:
                self.service(serv, "restart")      
            except:
                pass


    def getObj(self, objName):
        "Return object with specific object name"
        return eval("self."+objName+"Obj")


    def makePhoneBook(self):
        "Extract userinfo dics from ldap and make xmlphonebook out of them"
        if not self.ldapObj.getHost():
            self.ldapObj.setHost(self.__confVars["ldap"]["host"])

        if not self.ldapObj.getBaseDn():
            self.ldapObj.setBaseDn(self.__confVars["ldap"]["baseDn"])

        ldapReadDic = self.ldapObj.ldapRead(retrAttrs=self.__confVars["ldap"]["retrAttrs"])
        for contactDic in ldapReadDic:
            if 'telephoneNumber' in contactDic.keys():
                self.phonebookObj.addContact(contactDic)
        self.phonebookObj.xmlPhoneBook(self.__confVars["elastix"]["phonebookXmlPath"])
        self.phonebookObj.htmlPhoneBook(self.__confVars["elastix"]["ergoCompName"], ldapReadDic, self.__confVars["elastix"]["phonebookHtmlPath"], self.__confVars["elastix"]["cols"], self.__confVars["elastix"]["attrsLst"])

    def printFaxClientsIPs(self):
        "Print IPs for fax clients, in order to add them to elastix's 'allowance' box"        
        ipsStr = "\n".join(self.faxClientsObj.getFaxClientsIPs())

        filePath = 'faxClientsPath' in self.__confVars['elastix'].keys() and self.__confVars['elastix']['faxClientsPath']  or os.path.split(os.getcwd()+("/","")["libs" in os.getcwd()])[0]
        
        fp = open(os.path.join(filePath, "faxClientsIPs"), "w")
        fp.write(ipsStr+"\n")
        fp.close()


    def service(self, serviceName, task):
        "Start, stop, restart (etc) postfix service"
        ret = subcall(((self.__failsafe or os.path.join(self.__servicesPath, serviceName))+" "+task).split())

        if ret:
            print "Ret:"+ret
            if not self.__failsafe:
                self.__failsafe = "service "+serviceName
                self.service(serviceName, task)
        else:
            print "Ret:"+ret
            pass

        
    def setObj(self, objName):
        "Set the 'set' functions for object's variables"
        for varName in self.__confVars[objName].keys():
            exec "self."+objName+"Obj.set"+varName[0].upper()+varName[1:]+"("+repr(self.__confVars[objName][varName])+")"
    
    def setPhoneBookRefreshSchedule(self):
        "Add a crontab record, on when to refresh phonebook"        
        self.cronObj.addToCrontab()

    

