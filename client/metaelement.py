# -*- coding: utf-8 -*-
#
#            metaelement.py is part of MetaDoc (Client).
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

import logging
import xml.etree.ElementTree

class MetaElement(object):
    """ MetaElement - an individual element in the MetaDoc tree.

    An element roughly equates to a tag in the XML document. It contains 
    information about which subelements and attributes are allwoed. 

    This is a semi-abstract class (semi since we don't have the notion of
    abstract classes in python).

    """
    xml_tag_name = ""       # XML-tag name of the described element
    # The following three variables need only be implemented for root 
    # elements in the document. They will not be accessed for sub-entries. 
    update_handler = None   # Handler that will handle all recieved elements
                            # of this type (custom.abstract.MetaInput)
    site_handler = None     # Handler that populates information for this type
                            # from the site (custom.abstract.MetaOutput)
    url = None              # URL that will be accessed to send or recieve 
                            # information regarding this element type.

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
    def add_elements(self, elements):
        """ Adds a list of elements. """
        for element in elements:
            self.add_element(element)

    def clean(self):
        """ Runs clean functions on every attribute if they exist. """
        for attribute in self.attributes.keys():
            if hasattr(self, "clean_%s" % attribute):
                self.attributes[attribute] = getattr(self, "clean_%s" % attribute)(self.attributes[attribute])
    
    def find_id(self, locate_id):
        """ Attempts to find element with a given ID inside element. """
        # Is this the element?
        if "id" in self.attributes.keys():
            if self.attributes.get("id") == locate_id:
                return self
        # Check sub-elements for the id
        if self.sub_elements:
            for element in self.sub_elements:
                sub_element_found = element.find_id(locate_id)
                if sub_element_found:
                    return sub_element_found
        # Neither this or subelements has the ID, let's return nothing.
        return None

    @staticmethod
    def from_xml_element(xml_element, element_class):
        """ Creates a MetaElement from an xml.etree.ElementTree.Element instance. 
        
        Recursively checks for sub-elements from legal sub-classes.

        """
        # FIXME - Missing attribute error
        try:
            element = element_class(**xml_element.attrib)
        except TypeError, terr:
            logging.error("Unable to convert XML element \"%s\". Missing required attributes." % (xml_element.tag))
        if xml_element.text:
            element.text = xml_element.text
        for sub_class in element.legal_element_types:
            sub_elements = xml_element.findall(sub_class.xml_tag_name)
            for sub_element in sub_elements:
                element.sub_elements.append(MetaElement.from_xml_element(sub_element, sub_class))
        return element

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
