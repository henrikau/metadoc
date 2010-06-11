# -*- coding: utf-8 -*-
#
#            Project.py is part of MetaDoc (Client)
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

import metaelement
import xml.etree.ElementTree
from custom.updateprojects import UpdateProjects

class Projects(metaelement.MetaElement):
    """
    Information about projects tied to a system.
    """
    xml_tag_name = "projects"
    update_handler = UpdateProjects

    def __init__(self, type, date, fullUpdate=None):
        """
        init()
        """
        attributes = {
            'type': type,
            'date': date,
        }
        if fullUpdate:
            attributes['fullUpdate'] = fullUpdate
        super(Projects, self).__init__(Projects.xml_tag_name, attributes)
        self.legal_element_types = (ProjectEntry,)

class ProjectEntry(metaelement.MetaElement):
    xml_tag_name = "project_entry"
    
    def __init__(self, name, gid, status, account_nmb, valid_from, valid_to=None):
        attributes = {
            'name': name,
            'gid': gid,
            'status': status,
            'account_nmb': account_nmb,
            'valid_from': valid_from,
        }
        if valid_to:
            attributes['valid_to'] = valid_to
        super(ProjectEntry, self).__init__(ProjectEntry.xml_tag_name, attributes)
