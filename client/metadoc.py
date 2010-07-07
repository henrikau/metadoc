# -*- coding: utf-8 -*-
#
#            metadoc.py is part of MetaDoc (Client).
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
import version
import sys

class MetaDoc:
    """Class for handling the MetaDoc.

    A nice way of adding information and exporting to the MetaDoc-XML standard.

    """
    def __init__(self, site_name):
        """Sets the site name for the document and initializes the document's
        sub elements.

        @param site_name: Name of site described in document.
        @type site_name: String

        """
        self.site_name = site_name
        self.metaelements = []

    def _create_root(self):
        """Creates an lxml.etree.Element used as root for the document. """
        self.root = None
        self.root = lxml.etree.Element("MetaDoc",
                                        version=version.__version__,
                                        site_name=self.site_name)

    def reg_meta_element(self, me):
        """Add a new element to the base MetaDoc element. 
        
        @param me: Element to be added to the MetaDoc.
        @type me: L{MetaElement} sub class
        @return: bool indicating whether element was added.
        
        """
        if not me:
            return False
        if me.get_name():
            self.metaelements.append(me)
        return True

    def get_xml(self, with_id=True, pretty=False):
        """Generates a XML representation of the MetaDoc base on the MetaDoc 
        itself and any elements in self.metaelements.

        @param with_id: Indicates whether elements inside the MetaDoc should 
                        include their B{id} attribute.
        @type with_id: bool

        @param pretty: Indicates whether the returned string should include 
                        spacing for easier reading.
        @type pretty: bool

        @return: XML String representation of the MetaDoc.

        """
        self._create_root()
        for me in self.metaelements:
            self.root.append(me.get_xml_element(with_id))


        return lxml.etree.tostring(self.root, 
                encoding='utf-8', 
                pretty_print=pretty,
                xml_declaration=True)

    def find_id(self, locate_id):
        """Attempts to locate the element with a given ID inside the document. 
        
        @param locate_id: ID of element to be located.
        @type locate_id: String
        @return: L{MetaElement} sub class if element exists, or None
                if it doesn't.
        
        """
        for me in self.metaelements:
            element = me.find_id(locate_id)
            if element:
                return element
        return None

    def remove_element(self, element):
        """Attempts to remove element from sub elements. 
        
        @param element: Element that should be removed from the document.
        @type element: L{MetaElement} sub class
        @return: bool indicating whether element was found or not.
        
        """
        if element in self.metaelements:
            try:
                self.metaelements.remove(element)
            except ValueError, ve:
                # Will do nothing as it might still be in a sub-element
                pass
        for me in self.metaelements:
            if me.remove_element(element):
                return True
        return False

    def has_content(self):
        """Checks to see if there is any real content inside the MetaDoc.

        First checks whether it has any sub elements itself, if not, no content 
        is present. 
        If there are sub elements, must check to see if they contain any 
        content.

        @return: bool indicating whether document has content or not.

        """
        for me in self.metaelements:
            if me.has_content():
                return True
        return False

    def check_response(self, xml_response):
        """Function that checks the response from server.

        Can raise: L{InvalidXMLResponseError}, L{NoReceiptReturnedError} and 
        L{NotAllAcceptedError}.

        @param xml_response: Should be the XML response from the server when 
        self (this MetaDoc) was sent.
        @type xml_response: String

        """
        try:
            response = lxml.etree.fromstring(xml_response)
        except lxml.etree.XMLSyntaxError, e:
            logging.error("Error parsing server XML response: %s" % e)
            raise InvalidXMLResponseError()
        else:
            receipt = response.find("receipt")
            if receipt is not None:
                r_entries = receipt.findall("r_entry")
                for r_entry in r_entries:
                    element = self.find_id(r_entry.attrib.get("id"))
                    r_code = r_entry.attrib.get("code")
                    try:
                        r_code = int(r_code)
                    except ValueError, e:
                        logging.error(("Recieved a non-integer error code from "
                            "server: \"%s\".") % str(r_code))
                        continue
                    if not (r_code >= 1000 and r_code < 2000):
                        if r_code < 5000:
                            # Got an error that will NOT be fixed by 
                            # resending element. No point in caching.
                            self.remove_element(element)
                            sys.stderr.write(("Received critical error %d on "
                                "element \"%s\".\n") % (r_code, 
                                                        element.xml_tag_name))
                            sys.stderr.write("Please check log file for "
                                "more information.")
                        err_str = ("Error %d on \"%s\" element. Element "
                                    "attributes: %s") % (
                                        r_code,
                                        element.xml_tag_name,
                                        element.attributes
                                        )
                        if r_entry.attrib.get("note"):
                            err_str = "%s    \nError note: %s" % (err_str, 
                                            r_entry.attrib.get("note"))
                        if r_entry.text:
                            err_str = "%s    \nError message:\n%s" % (err_str, 
                                            r_entry.text)
                        logging.error(err_str)
                    else:
                        info_str = ("Element \"%s\" successfully added. "
                                "(Attributes: %s)") % (element.xml_tag_name, 
                                                        element.attributes)
                        logging.info(info_str)
                        self.remove_element(element)
            else:
                raise NoReceiptReturnedError()
        sub_element_count = 0
        for me in self.metaelements:
            sub_element_count = sub_element_count + len(me.sub_elements)
        if sub_element_count > 0:
            raise NotAllAcceptedError()

class Error(Exception):
    """ Base class for MetaDoc errors. """
    pass

class NoReceiptReturnedError(Error):
    """ Error raised when no receipt is returned. """
    pass

class InvalidXMLResponseError(Error):
    """ Error raised when repsonse XML cannot be parsed. """
    pass

class NotAllAcceptedError(Error):
    """ Error raised if not all elements are accepted. """
    pass
