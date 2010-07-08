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

import utils
import datetime

class MetaElement(object):
    """MetaElement - an individual element in the MetaDoc tree.

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
        """Initializes a MetaElement. 
        
        Sets the elements name (usually xml_tag_name) and attributes. 

        @param name: Name of the element.
        @type name: String
        @param attributes: Attributes for the element.
        @type attributes: dict

        """
        self.attributes = attributes
        self.name = name
        self.legal_element_types = ()
        self.sub_elements = []
        self.text = None

    def __str__(self):
        """We want the string representation of MetaElements to be its 
        XML tag. 
        
        """
        return "<%s>" % self.name

    def get_name(self):
        """Gets the name of the current element.
        
        @return: String containing name of element.
        
        """
        return self.name

    def get_attributes(self):
        """Get the attributes of the element. 
        
        @return: dict containing element attributes.
        
        """
        return self.attributes

    def get_xml_element(self, with_id=True):
        """Convert element into lxml.etree.Element.

        @param with_id: Indicates whether attribute B{id} of element and sub 
                        elements should be included.
        @type with_id: bool
        @return: lxml.etree.Element or None if unable to convert.
        
        """
        temp_id = False
        if not with_id:
            if "id" in self.attributes.keys():
                temp_id = self.attributes.get("id")
                del self.attributes['id']
        
        if not isinstance(self.attributes, dict):
            logging.info(("Attributes for \"%s\" is not dict. "
                        "Attempting to convert.") % (self.get_name()))
            try:
                self.attributes = dict(self.attributes)
            except ValueError, ve:
                logging.error("Cannot create XML element from \"%s\" because "
                            "attributes are of type \"%s\". Must be dict." % 
                            (self.get_name(), type(self.attributes)))
                return None
        try:
            element = lxml.etree.Element(self.get_name(), **self.attributes)
        except Exception, e:
            # FIXME - What errors can we produce? Should specify error.
            logging.error(("Unable to create XML element from "
                        "metaelement.MetaElement. XML tag \"%s\" with "
                        "attributes \"%s\".") % (self.get_name(),
                                                self.attributes))
            return None
        for el in self.sub_elements:
            append_element = el.get_xml_element(with_id)
            if append_element is not None:
                element.append(append_element)
            else:
                logging.error(("Unable to add sub-element \"%s\" to \"%s\" "
                            "because it could not retrieve XML element. ") % 
                            (el.xml_tag_name, self.xml_tag_name))
        
        if not with_id and temp_id:
            self.attributes['id'] = temp_id

        if self.text:
            element.text = self.text
        return element

    def add_element(self, element):
        """Add an entry to the element, this is typically a sub entry. 
        
        @param element: Element that should be added as a sub element of this.
        @type element: L{MetaElement} sub class
        @return: bool indicating whether element was added or not.
        
        """
        logging.debug("Adding element \"%s\" to \"%s\"." % 
                (element.xml_tag_name, self.xml_tag_name))
        valid_element = False
        for element_type in self.legal_element_types:
            if isinstance(element, element_type):
                valid_element = True
        if not valid_element:
            logging.error(("Recieved illegal element type \"%s\" for element "
                    "\"%s\". Allowed elements: \"%s\".") %
                    (type(element), type(self), self.legal_element_types))
            return False
        
        try:
            valid_element = element.clean()
        except Error, e:
            logging.error("%s" % e)
            return False
        else:
            if valid_element:
                logging.debug(("Recieved valid element \"%s\" to append "
                    "to \"%s\".") % (element.xml_tag_name, self.xml_tag_name))
                self.sub_elements.append(element)
                return True
            else:
                return False

    def add_elements(self, elements):
        """Adds a list of elements. 
        
        @param elements: List of elements to be added to this.
        @type elements: list of L{MetaElement} sub classes
        
        """
        for element in elements:
            self.add_element(element)

    def remove_element(self, element):
        """ Removes an element from list of sub elements. """
        if element in self.sub_elements:
            try:
                self.sub_elements.remove(element)
                return True
            except ValueError, ve:
                # Should occur only if element not in list, which we've 
                # checked for. But to be sure.
                logging.warning(("Attemting to remove non-existing element "
                    "from \"%s\".") % self.get_name())
                return False
        else:
            logging.warning(("Attemting to remove non-existing element from "
                "\"%s\".") % self.get_name())
            return False

    def has_content(self):
        """Checks whether there are any sub elements or text in this element.

        @return: bool indicating whether there are any sub elements in this 
                element, or if this element contains text.

        """
        if len(self.sub_elements) > 0:
            return True
        if self.text is not None:
            return True
        return False

    def clean(self):
        """Runs clean functions on every attribute if they exist. 
        
        clean functions raise L{IllegalAttributeError} (or sub class) when 
        unable to clean attribute values properly.

        @return: bool indicating whether this element is valid or not.

        """
        valid = True
        for attribute in self.attributes.keys():
            if hasattr(self, "clean_%s" % attribute):
                try:
                    self.attributes[attribute] = getattr(self, 
                        "clean_%s" % attribute)(self.attributes[attribute])
                except IllegalAttributeError, attrerr:
                    valid = False
                    logging.error("%s" % attrerr)
                else:
                    if not isinstance(self.attributes[attribute], basestring):
                        valid = False
                        logging.error(("Attribute \"%s\" on element \"%s\" is "
                            "not a string.") % (attribute, self.xml_tag_name))
            else:
                logging.debug(("Found no clean function for \"%s\" on element "
                    "\"%s\".") % (attribute, self.xml_tag_name))
        return valid
    def find_id(self, locate_id):
        """Attempts to find element with a given ID inside element. 
        
        @param locate_id: ID to look for.
        @type locate_id: String
        @return: L{MetaElement} sub class instance of element with the ID, 
                or None if no such element exist in this element.
        
        """
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

    def _clean_date(self, date, attribute_name, element):
        """Helper function that will clean a date. Returns a string in valid 
        RFC3339 form (with seconds granularity).

        @param date: Date to clean. Will convert either int, float, date or 
                    datetime to RFC3339 string.
        @type date: date, datetime, int, float, RFC3339 String
        
        @param attribute_name: Name of attribute being cleaned. Used for 
                            potential error message.
        @type attribute_name: string

        @param element: Name of element being cleaned. Used for potential
                        error message.
        @type element: string

        @return: string of RFC3339 date.

        """
        if isinstance(date, float) or isinstance(date, int) \
                or isinstance(date, datetime.datetime):
            return utils.date_to_rfc3339(date)
        elif isinstance(date, basestring):
            rfc_date = utils.rfc3339_to_date(date)
            if rfc_date is not False:
                return rfc_date

        raise IllegalAttributeValueError(attribute_name, 
                    date, 
                    ['float', 'datetime.datetime', 'RFC3339 String'], 
                    element)

    def _clean_types(self, value, allowed_types, attribute_name, element):
        """ Checks that `value` is one of `allowed_types`. """
        try:
            iter(allowed_types)
        except TypeError:
            try:
                if isinstance(value, allowed_types):
                    return True
            except TypeError:
                # If allowed_types is not a type, we will get a TypeError for 
                # get instance.
                logging.critical(("Element \"%s\" attempts to type check "
                    "against a non-type. Please check code.") % element)
        else:
            for allowed_type in allowed_types:
                try:
                    if isinstance(value, allowed_type):
                        return True
                except TypeError:
                    # See comment above.
                    logging.critical(("Element \"%s\" attempts to type check "
                        "against a non-type. Please check code.") % element)
        raise IllegalAttributeTypeError(attribute_name, 
                    type(value), 
                    element, 
                    allowed_types)

    def _clean_allowed_values(self, value, allowed_values, attribute_name, 
            element, case_sensitive = True):
        """ Checks value against a list of allowed values. """
        valid = True
        if case_sensitive:
            if value not in allowed_values:
                valid = False
        else:
            if value.lower() not in [a.lower() for a in allowed_values]:
                valid = False
        if not valid:
            raise IllegalAttributeValueError(attribute_name, 
                    value, 
                    allowed_values, 
                    element)
        return valid



    @staticmethod
    def from_xml_element(xml_element, element_class):
        """ Creates a MetaElement from an lxml.etree.Element instance. 
        
        Recursively checks for sub-elements from legal sub-classes.

        """
        try:
            element = element_class(**xml_element.attrib)
        except TypeError, terr:
            logging.error(("Unable to convert XML element \"%s\". "
                "Missing required attributes.") % (xml_element.tag))
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
                    logging.error("Unable to add sub element to \"%s\"." % 
                        element.xml_tag_name)
        # We'll check if there are subelements that should NOT be here
        for child in xml_element.getchildren():
            if child.tag not in [a.xml_tag_name for a in element.legal_element_types]:
                logging.warning(("Found an illegal sub-element of type \"%s\" "
                    "in element \"%s\".") % (child.tag, element.xml_tag_name))
        return element

# Error classes

class Error(Exception):
    """ Base Error class for MetaElements. """
    pass

class IllegalAttributeError(Error):
    """ Base class for problems with attributes. """
    pass

class IllegalAttributeValueError(IllegalAttributeError):
    """ Error given when an illegal value is passed as a value for an 
    attribute.

    """
    def __init__(self, attrib, used_value, allowed_values, element):
        self.attrib = attrib
        self.used_value = used_value
        self.allowed_values = allowed_values
        self.element = element
    def __str__(self):
        return ("Illegal value \"%s\" used for attribute \"%s\" in element "
            "\"%s\". Allowed values: %s.") % (self.used_value, self.attrib, 
                                            self.element, self.allowed_values)


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
        return ("Illegal type used for \"%s\" attribute in \"%s\". "
            "Allowed types: %s. Recieved type: \"%s\"") % (self.attrib, 
                                                    self.element, 
                                                    self.allowed_formats, 
                                                    self.used_type.__name__)

class IllegalElementError(Error):
    """ Error given when attempting to add a sub-element of a type that is not
    allowed by the element definition.

    """
    def __init__(self, element_type, sub_element_type, allowed_sub_elements):
        self.element_type = element_type
        self.sub_element_type = sub_element_type
        self.allowed_sub_elements = allowed_sub_elements

    def __str__(self):
        return ("Illegal sub-element for \"%s\". Got \"%s\", "
            "must be \"%s\".") % (self.element_type, self.sub_element_type, 
                                    self.allowed_sub_elements)

class NotImplementedError(Error):
    """ Error given when a call to an abstract function is made. """
    pass
