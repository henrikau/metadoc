# -*- coding: utf-8 -*-
#
#            utils.py is part of MetaDoc (Client).
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

import logging

import metadoc
from cacher import Cacher

def _singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@_singleton
class UniqueID(object):
    """ Singleton class to create unique IDs. """
    def __init__(self):
        """ Starts the ID counter at 0. """
        self.last_id = 0
    def get_id(self):
        """ Increments the ID counter and returns it. """
        self.last_id = self.last_id + 1
        return "%i" % self.last_id


def check_response(element_tag, md, xml_data):
    try:
        md.check_response(xml_data)
    except metadoc.NoReceiptReturnedError, nr:
        logging.error("Server returned no receipt. Caching data.")
        Cacher(element_tag, md)
    except metadoc.InvalidXMLResponseError, ir:
        logging.error("Server returned invalid receipt. Caching data.")
        Cacher(element_tag, md)
    except metadoc.NotAllAcceptedError, nar:
        logging.error("Not all elements accepted. Caching not accepted data.")
        Cacher(element_tag, md)
