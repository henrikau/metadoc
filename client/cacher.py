# -*- coding: utf-8 -*-
#
#            cacher.py is part of MetaDoc (Client).
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
import os
import lxml.etree

class Cacher(object):
    def __init__(self, element_type, metadoc = None):
        """ Receives a metadoc.MetaDoc that should be cached. """
        self.metadoc = metadoc
        self.file_path = "cache/%s.xml" % element_type
        self.element_type = element_type
        if not os.path.isdir("cache"):
            logging.info("Cache directory not present, attempting to create.")
            try:
                os.mkdir("cache")
            except IOError, e:
                logging.error("Unable to create cache directory. Please check access rights. (%s)" % e)
                return
            else:
                logging.info("Created cache directory.")

        if metadoc:
            cache_file = open(self.file_path, "w")
            cache_file.write(metadoc.get_xml(False))
            cache_file.close()

    def get_cache(self):
        """ Returns a lxml.etree.Element of self.element_type """
        cache_string = self._get_cache_string()
        if not cache_string:
            return None
        try:
            element = lxml.etree.fromstring(cache_string)
        except lxml.etree.XMLSyntaxError:
            logging.error("Cached file \"%s\" contains invalid XML." % self.file_path)
            return None
        return element.find(self.element_type)

    def remove_cache(self):
        """ Removes the file containing the cached data. """
        logging.info("Removing cached file \"%s\"." % self.file_path)
        try:
            # We've retrived the cached data, let's remove it so it wont 
            # be sent twice. If the data can't be sent it will be recached.
            os.remove(self.file_path)
        except IOError, e:
            logging.error("Unable to remove cache file \"%s\". Please remove to ensure data is not resent." % self.file_path)
            return

    def _get_cache_string(self):
        """ Returns cached data, if any. 
        
        Returns a string with the XML document if existent.

        """
        if not os.path.isfile(self.file_path):
            # No cached data for this type
            return None
        try:
            cached_file = open(self.file_path, "r")
        except IOError, e:
            logging.error("Found cache file \"%s\" but unable to open. Check access rights. (%s)" % (self.file_path, e))
            return None
        cached_string = cached_file.read()
        return cached_string
