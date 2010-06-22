# -*- coding: utf-8 -*-
#
#            projects/definition.py is part of MetaDoc (Client)
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
from custom.updateprojects import UpdateProjects
from projects.entries import ProjectEntry

class Projects(metaelement.MetaElement):
    """ Information about projects tied to a system. """
    xml_tag_name = "projects"
    update_handler = UpdateProjects
    url = "projects"

    def __init__(self, date, fullUpdate=None):
        """ Defines the projects XML tag.
        
        param:
        date            : Date of oldest element in set
        fullUpdate      : Whether the set is a complete set or just an update
                          (yes|no)
        
        """
        attributes = {
            'date': date,
        }
        if fullUpdate:
            attributes['fullUpdate'] = fullUpdate
        super(Projects, self).__init__(Projects.xml_tag_name, attributes)
        self.legal_types = ('request', 'update',)
        self.legal_fullUpdates = ('yes', 'no',)
        self.legal_element_types = (ProjectEntry,)
    def clean_type(self, type):
        """ Checks that `type` has a legal value. """
        self._clean_allowed_values(type, self.legal_types, 'type', self.xml_tag_name, False)
        return type
    def clean_fullUpdate(self, fullUpdate):
        """ Checks that `fullUpdate` has a legal value. """
        self._clean_allowed_values(fullUpdate, self.legal_fullUpdates, 'fullUpdate', self.xml_tag_name, False)
        return fullUpdate
