# -*- coding: utf-8 -*-
#
#            definition.py is part of MetaDoc (Client).
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
from custom.updateusers import UpdateUsers
from users.entries import UserEntry

class Users(metaelement.MetaElement):
    """
    List of users tied to a system.
    """
    xml_tag_name = "users"
    update_handler = UpdateUsers

    def __init__(self, type, date, fullUpdate = None):
        """
        """
        attributes = {
            'type': type,
            'date': date,
        }
        if fullUpdate:
            attributes['fullUpdate'] = fullUpdate
        super(Users, self).__init__(Users.xml_tag_name, attributes)
        self.legal_element_types = (UserEntry,)
