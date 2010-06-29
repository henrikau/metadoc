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

class MetaDoc:
    """ Class for handling the MetaDoc.

    A nice way of adding information and exporting to the MetaDoc-XML standard.

    """
    def __init__(self, fullUpdate=False):
        if fullUpdate:
            self.fullUpdate = "yes"
        else:
            self.fullUpdate = "no"
        self.metaelements = []

    def _create_root(self):
        self.root = None
        self.root = lxml.etree.Element("MetaDoc",
                                        version="1.0",
                                        fullUpdate=self.fullUpdate)

    def reg_meta_element(self, me):
        """ Add a new element to the base MetaDoc element. """
        if not me:
            return False
        if me.get_name():
            self.metaelements.append(me)
        return True

    def get_xml(self, with_id=True):
        """ Return the XML-string of the registred information.

        The result should be valid XML and ready to export to the recipient.

        """
        self._create_root()
        for me in self.metaelements:
            self.root.append(me.get_xml_element(with_id))


        return lxml.etree.tostring(self.root, 
                encoding='utf-8', 
                xml_declaration=True)

    def find_id(self, locate_id):
        """ Attempts to locate the element with a given ID. """
        for me in self.metaelements:
            element = me.find_id(locate_id)
            if element:
                return element
        return None

    def remove_element(self, element):
        """ Attempts to remove element from sub-elements. """
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

        First checks whether it has any subelements itself, if not, no content 
        is present. 
        If there are subelements, must check to see if they contain any content.
        """
        for me in self.metaelements:
            if me.has_content():
                return True
        return False

    def check_response(self, xml_response):
        """ Function that checks the response from server.
        xml_response should be the XML response from the server when self was 
        sent.

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
                        err_str = ("Error %s on \"%s\" element. Element "
                                    "attributes: %s") % (
                                        r_entry.attrib.get("code"),
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
