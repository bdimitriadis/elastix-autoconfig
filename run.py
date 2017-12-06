#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: run.py
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


from libs.elastixConfs import ElastixConfs

elstxObj = ElastixConfs()
elstxObj.fixAllConfs()
elstxObj.setPhoneBookRefreshSchedule()
elstxObj.makePhoneBook()
#elstxObj.printFaxClientsIPs()

