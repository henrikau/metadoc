# -*- coding: utf-8 -*-
#
#            MetaDoc.py is part of MetaDoc (Client).
#
# All of MetaDoc is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# MetaDoc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MetaDoc.  If not, see <http://www.gnu.org/licenses/>.
# The API interface
import xml.etree.ElementTree

class MetaDoc:
    """
    Class for handling the MetaDoc.

    A nice way of adding information and exporting to the MetaDoc-xml standard.
    """
    def __init__(self, fullUpdate=False):
        if fullUpdate:
            self.fullUpdate = "yes"
        else:
            self.fullUpdate = "no"
        self.root = xml.etree.ElementTree.Element("MetaDoc",
                                                  version="1.0",
                                                  fullUpdate=self.fullUpdate)
        self.mes = {}

    def regMetaElement(self, me):
        """
        regMetaElement: add a new element to the base MetaDoc elemeent.
        """
        if not me:
            return False
        if me.getElement():
            self.mes[me.getName()] = me.getElement()
        return True

    def getXML(self):
        """
        Return the XML-string of the registred information.

        The result should be valid XML and ready to export to the recipient.
        """
        if 'users' in self.mes:
            self.root.append(self.mes['users'])
        if 'projects' in self.mes:
            self.root.append(self.mes['projects'])
        if 'allocations' in self.mes:
            self.root.append(self.mes['allocations'])
        if 'events' in self.mes:
            self.root.append(self.mes['events'])
        if 'siteInfo' in self.mes:
            self.root.append(self.mes['siteInfo'])
        return xml.etree.ElementTree.tostring(self.root, "UTF-8")


