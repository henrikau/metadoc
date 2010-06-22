# -*- coding: utf-8 -*-
#
#            users/entries.py is part of MetaDoc (Client).
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

import metaelement

class UserEntry(metaelement.MetaElement):
    """ Information about each specific user. """
    xml_tag_name = "user_entry"

    def __init__(self, username, uid=None, full_name=None, password=None, 
                    default_group=None, special_path=None, shell=None, 
                    email=None, phone=None, status=None, org=None):
        """ Defines the user_entry XML tag.

        param:
        username        : User's username
        uid             : UserID of user
        full_name       : Full name of the user
        password        : Password hash of initial password
        default_group   : Default group of user
        special_path    : Path of user if needed
        shell           : Shell for user
        email           : Supplied email address of user
        phone           : Supplied phone number of user
        status          : Status of user, should be interpreted as 
                          modification if nothing is set.
                          (new|existing|deactivate|delete)
        """
        attributes = {'username': username}
        if uid is not None:
            attributes['uid'] = uid
        if full_name is not None:
            attributes['full_name'] = full_name
        if password is not None:
            attributes['password'] = password
        if default_group is not None:
            attributes['default_group'] = default_group
        if special_path is not None:
            attributes['special_path'] = special_path
        if shell is not None:
            attributes['shell'] = shell
        if email is not None:
            attributes['email'] = email
        if phone is not None:
            attributes['phone'] = phone
        if status is not None:
            attributes['status'] = status
        if org is not None:
            attributes['org'] = org
        super(UserEntry, self).__init__(UserEntry.xml_tag_name, attributes)

    def clean_uid(self, uid):
        """ Converts uid to string if int. """
        if isinstance(uid, int):
            uid = "%d" % uid
        return uid

    def clean_phone(self, phone):
        """ Converts phone to string if int. """
        if isinstance(phone, int):
            phone = "%d" % phone
        return phone
