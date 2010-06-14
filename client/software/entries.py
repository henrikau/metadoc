# -*- coding: utf-8 -*-
#
#            entries.py is part of MetaDoc (Client).
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

class SoftwareEntry(metaelement.MetaElement):
    """ Registers software_entry and packs to XML. """
    xml_tag_name = "sw_entry"

    def __init__(self, program_name, version, license = None, info_url = None):
        self.attributes = {
            'progName': program_name,
            'version': version,
        }
        if license:
            self.attributes['version'] = version
        if info_url:
            self.attributes['infoURL'] = info_url

        super(SoftwareEntry, self).__init__(SoftwareEntry.xml_tag_name, self.attributes)
