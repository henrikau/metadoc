#
#            software.py is part of MetaDoc (Client).
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
import xml.etree.ElementTree

class Software(metaelement.MetaElement):
    """ Registers software and packs to XML.

    """
    def __init__(self):
        super(Software, self).__init__("software")
        self.legal_element_types = (SoftwareEntry,)

class SoftwareEntry(metaelement.MetaElement):
    def __init__(self, program_name, version, license = None, info_url = None):
        self.attributes = {
            'progName': program_name,
            'version': version,
        }
        if license:
            self.attributes['version'] = version
        if info_url:
            self.attributes['infoURL'] = info_url

        super(SoftwareEntry, self).__init__("sw_entry", self.attributes)
