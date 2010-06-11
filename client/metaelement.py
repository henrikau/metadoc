# -*- coding: utf-8 -*-
#
#            MetaElement.py is part of MetaDoc (Client).
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

class Error(Exception):
    """
    Base Error class for MetaElements.
    """
    pass

class IllegalAttributeValueError(Error):
    """
    Error given when an illegal value is passed as a value for an attribute.
    """
    def __init__(self, attrib, used_value, allowed_values, element):
        self.attrib = attrib
        self.used_value = used_value
        self.allowed_values = allowed_values
        self.element = element
    def __str__(self):
        return repr("Illegal value \"%s\" used for attribute \"%s\" in element \"%s\". Allowed values: %s." % (self.used_value, self.attrib, self.element, self.allowed_values))


class IllegalAttributeTypeError(Error):
    """
    Error given when an attribute is passed a value in an illegal format. 
    """
    def __init__(self, attrib, used_type, element, allowed_formats):
        self.attrib = attrib
        self.allowed_formats = allowed_formats
        self.used_type = used_type
        self.element = element
    def __str__(self):
        return repr("Illegal type used for \"%s\" attribute in \"%s\". Allowed types: %s. Recieved type: \"%s\"" % (self.attrib, self.element, self.allowed_formats, self.used_type.__name__))

class MetaElement(object):
    """
    MetaElement - an individual element in the MetaDoc tree.

    This is a semi-abstract class (semi since we don' have the notion of
    abstract classes in python).
    """
    def __init__(self, name):
        self.attribs        = None
        self.element        = None
        self.name           = name
        self.entryAttribs   = ()

    def getName(self):
        """
        getName - return the name of the element
        """
        return self.name

    def getElement(self):
        """
        element is an xml.etree.Element with the values. It can be a hierarchy
        """
        if self.element:
            return self.element

    def addEntry(self):
        """
        addEntry: add an entry to the element, this is typically a sub-entry.

        At the MetaElement level, this will raise an error, so classes
        inheriting from MetaElement must override this method.
        """
        raise Exception("%s has not implemented addEntry, and function cannot be used!" % self.name)

    def checkEntries(self, *args, **kwargs):
        """
        Checks the recieved attributes for the entry against entryAttribs

        Each attribute recieved will be cleaned with it's respective clean function. 
        Raises an error if any required attributes are missing.
        """
        attributeList = {}
        for attrib in self.entryAttribs:
            if attrib['name'] in kwargs.keys():
                if attrib['cleanFunction'] is not None:
                    # FIXME - Catch getattr error
                    attributeList[attrib['name']] = getattr(self, attrib['cleanFunction'])(kwargs[attrib['name']])
            else:
                if attrib['required']:
                    # We're missing a required attribute
                    raise Exception("Entry added to \"%s\" is missing required attribute \"%s\"." % (self.name, attrib['name']))
        return attributeList
