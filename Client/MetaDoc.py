# -*- coding: utf-8 -*-
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


