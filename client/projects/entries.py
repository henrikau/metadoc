# -*- coding: utf-8 -*-
#
#            projects/entries.py is part of MetaDoc (Client)
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
from users.entries import UserEntry

class ProjectEntry(metaelement.MetaElement):
    """ Information about each specific project. """
    xml_tag_name = "project_entry"
    
    def __init__(self, name, status, account_nmb, valid_from, abbrev=None, 
                    valid_to=None, responsible_person=None, gid=None):
        """ Defines the project_entry XML tag.

        param:
        name            : Name of the project
        gid             : Group-id of the project
        valid_from      : From when the project is valid
        valid_to        : When the project should terminate
        status          : Status of the project (new|existing|delete)

        """
        attributes = {
            'name': name,
            'status': status,
            'account_nmb': account_nmb,
            'valid_from': valid_from,
        }
        if abbrev is not None:
            attributes['abbrev'] = abbrev
        if valid_to is not None:
            attributes['valid_to'] = valid_to
        if responsible_person is not None:
            attributes['responsible_person'] = responsible_person
        if gid is not None:
            attributes['gid'] = gid
        super(ProjectEntry, self).__init__(ProjectEntry.xml_tag_name, attributes)
        self.legal_element_types = (RemarksEntry, DescriptionEntry,UserEntry,)

    def get_remarks(self):
        """ Returns remarks, if any. """
        for el in self.sub_elements:
            if isinstance(el, RemarksEntry):
                return el.text
        return None

    def get_description(self):
        """ Returns description, if any. """
        for el in self.sub_elements:
            if isinstance(el, DescriptionEntry):
                return el.text
        return None

    def get_user_list(self):
        user_list = []
        for el in self.sub_elements:
            if isinstance(el, UserEntry):
                user_list.append(el)
        return user_list
    def clean_gid(self, gid):
        """ Converts gid to string if int. If neither string nor int, 
        raise an IllegalAttributeTypeError.

        """
        if isinstance(gid, int):
            gid = "%d" % gid
        return gid
    def clean_valid_from(self, valid_from):
        """ Checks that `valid_from` is RFC3339 compliant. """
        valid_from = self._clean_date(valid_from, 'valid_from', self.xml_tag_name)
        return valid_from
    def clean_valid_to(self, valid_to):
        """ Checks that `valid_to` is RFC3339 compliant. """
        valid_to = self._clean_date(valid_to, 'valid_to', self.xml_tag_name)
        return valid_to

class RemarksEntry(metaelement.MetaElement):
    xml_tag_name = "remarks"

    def __init__(self):
        super(RemarksEntry, self).__init__(RemarksEntry.xml_tag_name)

class DescriptionEntry(metaelement.MetaElement):
    xml_tag_name = "description"

    def __init__(self):
        super(DescriptionEntry, self).__init__(DescriptionEntry.xml_tag_name)
