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
import lxml.etree

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
    resend_cache = True     # If any cached data for this element should be
                            # sent when another call to send this type is run.

    def __init__(self, name, attributes = {}):
        """ Initializes a MetaElement. 
        
        Sets the elements name (usually xml_tag_name) and attributes. 

        """
        for attrib in attributes.keys():
            attributes[attrib] = str(attributes[attrib])
        self.attributes = attributes
        self.name = name
        self.legal_element_types = ()
        self.sub_elements = []
        self.text = None

    def get_name(self):
        """ Return the name of the element. """
        return self.name

    def get_attributes(self):
        """ Returns the attributes of the element. """
        return self.attributes

    def get_xml_element(self, with_id=True):
        """ element is an lxml.etree.Element with the values. 
        
        It can be a hierarchy 
        
        """
        temp_id = False
        if not with_id:
            if "id" in self.attributes.keys():
                temp_id = self.attributes.get("id")
                del self.attributes['id']
        
        if not isinstance(self.attributes, dict):
            logging.info("Attributes for \"%s\" is not dict. Attempting to convert." % (self.get_name()))
            try:
                self.attributes = dict(self.attributes)
            except ValueError, ve:
                logging.error("Cannot create XML element from \"%s\" because attributes are of type \"%s\". Must be dict." % (self.get_name(), type(self.attributes)))
                return None
        try:
            element = lxml.etree.Element(self.get_name(), **self.attributes)
        except Exception, e:
            # FIXME - What errors can we produce?
            logging.error("Unable to create XML element from metaelement.MetaElement. XML tag \"%s\" with attributes \"%s\"." % (self.get_name(), self.attributes))
            return None
        for el in self.sub_elements:
            append_element = el.get_xml_element(with_id)
            if append_element is not None:
                element.append(append_element)
            else:
                logging.error("Unable to add sub-element \"%s\" to \"%s\" because it could not retrieve XML element. " % (el.xml_tag_name, self.xml_tag_name))
        
        if not with_id and temp_id:
            self.attributes['id'] = temp_id

        if self.text:
            element.text = self.text
        return element

    def add_element(self, element):
        """ Add an entry to the element, this is typically a sub-entry. """
        valid_element = False
        for element_type in self.legal_element_types:
            if isinstance(element, element_type):
                valid_element = True
        if not valid_element:
            logging.error("Recieved illegal element type \"%s\" for element \"%s\". Allowed elements: \"%s\"." % (type(element), type(self), self.legal_element_types))
            return False
        
        element.clean()
        self.sub_elements.append(element)

    def add_elements(self, elements):
        """ Adds a list of elements. """
        for element in elements:
            self.add_element(element)

    def remove_element(self, element):
        """ Removes an element from list of sub-elements. """
        if element in self.sub_elements:
            try:
                self.sub_elements.remove(element)
                return True
            except ValueError, ve:
                # Should occur only if element not in list, which we've 
                # checked for. But to be sure.
                logging.warning("Attemting to remove non-existing element from \"%s\"." % self.get_name())
                return False
        else:
            logging.warning("Attemting to remove non-existing element from \"%s\"." % self.get_name())
            return False

    def clean(self):
        """ Runs clean functions on every attribute if they exist. """
        for attribute in self.attributes.keys():
            if hasattr(self, "clean_%s" % attribute):
                try:
                    self.attributes[attribute] = getattr(self, "clean_%s" % attribute)(self.attributes[attribute])
                except IllegalAttributeError, attrerr:
                    logging.error("%s" % attrerr)
    
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
        """ Creates a MetaElement from an lxml.etree.Element instance. 
        
        Recursively checks for sub-elements from legal sub-classes.

        """
        try:
            element = element_class(**xml_element.attrib)
        except TypeError, terr:
            logging.error("Unable to convert XML element \"%s\". Missing required attributes." % (xml_element.tag))
            return None
        if xml_element.text:
            element.text = xml_element.text
        for sub_class in element.legal_element_types:
            sub_elements = xml_element.findall(sub_class.xml_tag_name)
            for sub_element in sub_elements:
                me = MetaElement.from_xml_element(sub_element, sub_class)
                if me is not None:
                    element.sub_elements.append(me)
                else:
                    logging.error("Unable to add sub element to \"%s\"." % element.xml_tag_name)
        return element

# Error classes

class Error(Exception):
    """ Base Error class for MetaElements. """
    pass

class IllegalAttributeValueError(Error):
    """ Error given when an illegal value is passed as a value for an 
    attribute.

    """
    def __init__(self, attrib, used_value, allowed_values, element):
        self.attrib = attrib
        self.used_value = used_value
        self.allowed_values = allowed_values
        self.element = element
    def __str__(self):
        return repr("Illegal value \"%s\" used for attribute \"%s\" in element \"%s\". Allowed values: %s." % (self.used_value, self.attrib, self.element, self.allowed_values))


class IllegalAttributeError(Error):
    """ Base class for problems with attributes. """
    pass


class IllegalAttributeTypeError(IllegalAttributeError):
    """ Error given when an attribute is passed a value in an illegal 
    format. 

    """
    def __init__(self, attrib, used_type, element, allowed_formats):
        self.attrib = attrib
        self.allowed_formats = allowed_formats
        self.used_type = used_type
        self.element = element
    def __str__(self):
        return repr("Illegal type used for \"%s\" attribute in \"%s\". Allowed types: %s. Recieved type: \"%s\"" % (self.attrib, self.element, self.allowed_formats, self.used_type.__name__))

class IllegalElementError(Error):
    """ Error given when attempting to add a sub-element of a type that is not
    allowed by the element definition.

    """
    def __init__(self, element_type, sub_element_type, allowed_sub_elements):
        self.element_type = element_type
        self.sub_element_type = sub_element_type
        self.allowed_sub_elements = allowed_sub_elements

    def __str__(self):
        return repr("Illegal sub-element for \"%s\". Got \"%s\", must be \"%s\"." % (self.element_type, self.sub_element_type, self.allowed_sub_elements))

class NotImplementedError(Error):
    """ Error given when a call to an abstract function is made. """
    pass
