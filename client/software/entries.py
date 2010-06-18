# -*- coding: utf-8 -*-
#
#            software/entries.py is part of MetaDoc (Client).
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
#

import metaelement
from utils import UniqueID

class SoftwareEntry(metaelement.MetaElement):
    """ Registers software_entry and packs to XML. """
    xml_tag_name = "sw_entry"

    def __init__(self, progName, version, license = None, infoURL = None):
        """ Defines the sw_entry XML tag.

        param:
        progName                : Name of the software
        version                 : Software version
        license                 : Software license
        infoURL                 : URL with more information about the software.
        """
        u = UniqueID()
        self.attributes = {
            'progName': progName,
            'version': version,
            'id': u.get_id()
        }
        if license:
            self.attributes['version'] = version
        if infoURL:
            self.attributes['infoURL'] = infoURL

        super(SoftwareEntry, self).__init__(SoftwareEntry.xml_tag_name, self.attributes)

    def clean_version(self, version):
        """ Converts version to string if int or float. """
        if isinstance(version, int):
            version = "%d" % version
        elif isinstance(version, float):
            version = "%f" % version
        return version

    def clean_infoURL(self, infoURL):
        """ Checks whether infoURL is up. """
        # FIXME - Implement?
        return infoURL
