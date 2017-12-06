#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: httpdConfs.py
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


from genericConfs import GenericConf
import os

class HttpdConfs:
    def __init__(self):
        self.__phpFilePath = os.path.join(os.path.sep, "etc", "php.ini")
        self.__mainFilePath = os.path.join(os.path.sep, "var", "www", "html", "mail", "config", "main.inc.php")
        self.__emailFilePath = os.path.join(os.path.sep, "var", "www", "html", "configs", "email.conf.php")
    
        self.__phpObj = GenericConf(self.__phpFilePath, "=", ";")
        self.__mainObj = GenericConf(self.__mainFilePath, "=", "//", ";")
        self.__emailObj = GenericConf(self.__emailFilePath, "=", "//", ";")

        self.__httpsExcludePhoneBook()

    def __httpsExcludePhoneBook(self):
        "Modify elastix.conf to exclude phonebook path from https rule (use simple http)"
        filePath = os.path.join(os.path.sep, "etc", "httpd", "conf.d", "elastix.conf")
        fp = open(filePath, "r")
        lines = fp.readlines()
        fp.close()
       
        ruleStr = "RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}"
        condLine = "RewriteCond %{REQUEST_URI} !^/phonebook/\n"

        indx = ([lines.index(line) for line in lines if ruleStr in line]+[None])[0]		

        if indx:
            condLine = condLine.rjust(lines[indx].count(" ")-ruleStr.count(" ")+len(condLine))
            if condLine not in lines:
                lines.insert(indx, condLine) # Insert condition line before rewriterule for https
            fp = open(filePath, "w")
            fp.writelines(lines)
            fp.close()

    def commit(self):
        self.__phpObj.commit()
        self.__mainObj.commit()
        self.__emailObj.commit()

    def getCreateDefaultFolders(self):
        return self.__mainObj.getValue("$rcmail_config['create_default_folders']")

    def getMailHost(self):
        return self.__emailObj.getValue("$GLOBALS['CYRUS']")

    def getPostMaxSize(self):
        return self.__phpObj.getValue("post_max_size")

    def getUploadMaxFileSize(self):
        return self.__phpObj.getValue("upload_max_filesize")

    def setCreateDefaultFolders(self, state = True):
        self.__mainObj.setValue("$rcmail_config['create_default_folders']", state)

    def setMailHost(self, host = "localhost"):
        mailHostVal = self.getMailHost().replace("$host","'%s'"%host)
        self.__emailObj.setValue("$GLOBALS['CYRUS']", mailHostVal)

    def setPostMaxSize(self, postMax="100M"):
        self.__phpObj.setValue("post_max_size", postMax)

    def setUploadMaxFileSize(self, uploadMax="100M"):
        self.__phpObj.setValue("upload_max_filesize", uploadMax)

