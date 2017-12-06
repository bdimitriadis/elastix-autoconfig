#!/usr/bin/env python
#-*- coding: UTF-8 -*-
# File: phonebookCreator.py
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
    import xml.etree.cElementTree as ET
except ImportError:
    try:
        import cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET        

class PhoneBook:
    def __init__(self):
        self.__root = ET.Element("AddressBook")
        self.__contacts = {}
        
        
    def __greek2Greeklish(self, toTranslate):
        "Translate greek userinfo (names or surnames) to greeklish"
        lowerGreekTbl = "αβγδεζηθικλμνξοπρσςτυφχψωάέήίόύώ".decode("utf8")       
        upperGreekTbl = lowerGreekTbl.upper()
        greekTbl = lowerGreekTbl+upperGreekTbl

        lowerEngTbl = "avgdeziwiklmnjoprsstufxcoaeiiouo".decode("utf8")
        upperEngTbl = lowerEngTbl.upper()
        engTbl = lowerEngTbl+upperEngTbl

        transTbl = dict(zip(greekTbl,engTbl))    



        consonants = "vgdzwkmnjpstfxc"
        vowels = "aeiou"
        vowelsXou = "aei"
        
        doubles = dict((key+key,key) for key in consonants)
        vowU = [vow+"u" for vow in vowelsXou]
        vowUf = dict((vu+cons, vu.replace("u","f")+cons) for vu in vowU for cons in consonants)
        vowUv = dict((vu+vr, vu.replace("u","v")+vr) for vu in vowU for vr in vowels+"r"+"l")
        consU = dict((c+"u", (c+"u").replace("u","i")) for c in consonants+"r"+"l")
        



        translated = "".join(letter in transTbl.keys() and transTbl[letter] or letter for letter in toTranslate.decode("utf8"))

        postProc = {"w":"th", "j":"ks", "c":"ps", "ei":"i", "oi":"i", "gk":"g"}
        postProc.update(doubles)
        postProc.update(vowUf)
        postProc.update(vowUv)
        postProc.update(consU)
        postProc.update(dict((key.capitalize(),postProc[key].capitalize()) for key in postProc.keys()))

        transl = translated.decode("utf8")
        import re
        for pat in postProc.keys():
            transl = re.sub(pat, postProc[pat], transl)

        #translated = "".join(letter in postProc.keys() and postProc[letter] or letter for letter in translated.decode("utf8"))

        return transl

    def addContact(self, contactDic):
        "Add contact (first, last name and phone number) to phonebook"
        if 'displayName' not in contactDic.keys():
            return
        dispName = contactDic['displayName'][0].split(" ", 1)
        dispName = dispName + [""]
        firstName = dispName[1] #'givenName' in contactDic.keys() and self.__greek2Greeklish("".join(contactDic['givenName'])) or ""
        lastName = dispName[0] #'sn' in contactDic.keys() and  self.__greek2Greeklish("".join(contactDic['sn'])) or ""     
        phone = "".join(contactDic['telephoneNumber'])

        #tmpKey = lastName+" "+firstName
        #if len(phone)<=5:
        self.__contacts[lastName+" "+firstName] = [lastName, firstName, phone, u'1']

    def updateContactIndex(self, lastName, firstName, accountIndx):
        "Update contact's account index, if more than one ring groups are used"
        self.__contacts[lastName+" "+firstName][-1] = str(accountIndx)


    def xmlPhoneBook(self, xmlFileName):
        "Export phonebook to xml"
        import os
        try:
            os.makedirs(os.path.dirname(xmlFileName))
        except OSError:
            pass

        for key in sorted(self.__contacts.keys()):
            ct = ET.SubElement(self.__root, 'Contact')

            ln = ET.SubElement(ct, 'LastName')
            ln.text = self.__contacts[key][0]

            fn = ET.SubElement(ct, 'FirstName')
            fn.text = self.__contacts[key][1]

            ph = ET.SubElement(ct, 'Phone') 
            pn = ET.SubElement(ph, 'phonenumber')
            i = [0,2][len(self.__contacts[key][2]) == 5]
            pn.text = self.__contacts[key][2][i:]

            ai = ET.SubElement(ph, 'accountindex')
            ai.text = self.__contacts[key][3]

        tree = ET.ElementTree(self.__root)      
        tree.write(xmlFileName)


    def htmlPhoneBook(self, ergoCompName, phonesDict, fileName, cols = 3, attrsLst=['cn', 'telephoneNumber']):
        """"ErgoCompName is ergo's or company's name, phonesDict is the dictionary containing all the necessary info (phones, names, etc.), 
        cols is the number of columns for our html phonebook, atrrsLst is a list containing the attributes we want to retrieve from ldap info"""
        tblsStList = []
        tbl2tds = {}

        phonesDict = [el for el in phonesDict if 'telephoneNumber' in el.keys()]

        tdTmpl = "<td><center><cellVal></center></td>"
                        
        tblTmpl = """<table id="<ou>" border="2" cellpadding="5" width="100%%">
                        <tr>
                           <th colspan=%s><ou></th>
                        </tr>
                        <cellsOfTable>    
            </table><br/>""" %(len(attrsLst))

        from operator import itemgetter
        phonesDict.sort(key = lambda x:int(x['telephoneNumber'][0].replace("-","").replace(" ","").replace(",","")))
        sortedKeys=[]

        phonesLst = [el['telephoneNumber'][0] for el in phonesDict]
        phones=[phonesDict.pop(phonesLst.index(phonesLst.pop(phonesLst.index(el))))['telephoneNumber'][0] for el in phonesLst if phonesLst.count(el)>1]
       
        prefixes = [] 
        for dic in phonesDict:
            prefix = ""
            prefixTd = ""
            if 'ou' not in dic.keys() and attrsLst!=list(set(attrsLst)&set(dic.keys())):
                continue

            if dic['ou'][0] not in sortedKeys:
                sortedKeys.append(dic['ou'][0])
            if  dic['ou'][0]=="Γραμματεία": #or dic['telephoneNumber'][0] in phones:
                dic['cn'][0] = dic['ou'][0] +" "+ ergoCompName

            if len(dic['telephoneNumber'][0]) == 5:
                prefix = dic['telephoneNumber'][0][0:2]
                dic['telephoneNumber'][0]=dic['telephoneNumber'][0][2:]
            if prefix and prefix not in prefixes:
                prefixTd = "<tr><th colspan=\"2\">Πρόθεμα: %s</th></tr>"%(prefix)
                prefixes.append(prefix)
            tbl2tds[dic['ou'][0]]=[dic['ou'][0] in tbl2tds and tbl2tds[dic['ou'][0]] or ""][0]+prefixTd+"<tr>"+"\n".join([tdTmpl.replace("<cellVal>", dic[key][0]) for key in attrsLst if dic[key] not in dic.values()[:dic.keys().index(key)]])+"</tr>"

        for key in sortedKeys:
            tblElmnt = tblTmpl.replace('<ou>', key).replace("<cellsOfTable>", tbl2tds[key])        
            tblsStList.append(tblElmnt)

        from math import ceil
        
        steps = int(ceil(len(tblsStList)/float(cols)))

        for i in xrange(0,cols):
            tblsStList.insert(i*(steps+1)+i,"<td valign=\"top\">")
            tblsStList.insert((i+1)*(steps+1)+i,"</td>")       

        htmlTmpl = """<!DOCTYPE html>
            <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <title>Κατάλογος εσωτερικών και εξωτερικών τηλεφώνων %s</title>
            </head>
            <body>
                <center><h3>ΚΑΤΑΛΟΓΟΣ ΕΣΩΤΕΡΙΚΩΝ ΚΑΙ ΕΞΩΤΕΡΙΚΩΝ ΤΗΛΕΦΩΝΩΝ %s</h3></center>
                <br/>
                <center>
                <table border="1" cellpadding="15">        
                    %s     
                </table>
                <br/>
                </center>
            </body>
            </html>
            """%(ergoCompName, ergoCompName.upper(), "\n".join(tblsStList))

        fp=open(fileName, "w")
        fp.write(htmlTmpl)
        fp.close()

        return htmlTmpl
        
            

