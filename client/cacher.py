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

class Cacher(object):
    def __init__(self, file_type, metadoc = None):
        """ Receives a metadoc.MetaDoc that should be cached. """
        self.metadoc = metadoc
        self.file_path = "cache/%s.xml" % file_type
        if not os.path.isdir("cache"):
            logging.info("Cache not preset, attempting to create.")
            try:
                os.mkdir("cache")
            except:
                # FIXME - What errors can this produce?
                return
            else:
                logging.info("Created cache directory.")

        # Cache dir should exist when we've reached this point 
        # FIXME - File already exists, we do not want to overwrite
        cache_file = open(self.file_path, "w")
        cache_file.write(metadoc.get_xml())
        cache_file.close()
