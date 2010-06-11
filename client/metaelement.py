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

import xml.etree.ElementTree

class MetaElement(object):
    """ MetaElement - an individual element in the MetaDoc tree.

    An element roughly equates to a tag in the XML document. It contains 
    information about which subelements and attributes are allwoed. 

    This is a semi-abstract class (semi since we don't have the notion of
    abstract classes in python).

    """
    def __init__(self, name, attributes = {}):
        self.attributes = attributes
        self.name = name
        self.legal_element_types = ()
        self.sub_elements = []
        self.text = None
        
        self.create_xml_element()

    def get_name(self):
        """ Return the name of the element. """
        return self.name

    def get_attributes(self):
        """ Returns the attributes of the element. """
        return self.attributes

    def create_xml_element(self):
        """ Creates the XML-element """
        # FIXME - Catch exceptions
        # Return None if exception?
        self.element = xml.etree.ElementTree.Element(self.get_name(), **self.attributes)
        if self.text:
            self.element.text = self.text

    def get_xml_element(self):
        """ element is an xml.etree.Element with the values. It can be a hierarchy """
        if not self.element:
            self.create_xml_element()
        return self.element

    def add_element(self, element):
        """ add_element: add an entry to the element, this is typically a sub-entry. """
        valid_element = False
        for element_type in self.legal_element_types:
            if isinstance(element, element_type):
                valid_element = True
        if not valid_element:
            raise Exception("Illegal element type")
        
        element.clean()
        self.sub_elements.append(element)
        self.element.append(element.get_xml_element())

    def clean(self):
        """ Runs clean functions on every attribute if they exist. """
        for attribute in self.attributes.keys():
            if hasattr(self, "clean_%s" % attribute):
                self.attributes[attribute] = getattr(self, "clean_%s" % attribute)(self.attributes[attribute])

# Error classes

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


class NotImplementedError(Error):
    """ Error given when a call to an abstract function is made. """
    pass
