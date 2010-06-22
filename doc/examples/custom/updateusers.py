# -*- coding: utf-8 -*-
#
#            custom/updateusers.py is part of MetaDoc (Client).
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
# The API interface

import logging

from abstract import MetaInput

class UpdateUsers(MetaInput):
    """ Class for processing recieved user data. """
    def process(self):
        """ Called when user data is parsed and should be processed for the 
        site.

        Example of a process call that creates a shadow file from the recieved 
        user data.

        """
        file_lines = []
        # Loop through all <users> tags. Should only be one.
        for item in self.items:
            # Loop through all <user_entry> tags.
            for user in item.sub_elements:
                # Create a shadowfile line for each user.
                file_line = "%s:%s:%s:%s:%s,%s,%s,%s,%s:%s:%s\n" % (
                        user.attributes.get("username", ""),
                        user.attributes.get("password", ""),
                        user.attributes.get("uid", ""),
                        user.attributes.get("default_group", ""),
                        user.attributes.get("full_name", ""),
                        user.attributes.get("org", ""),
                        user.attributes.get("phone", ""),
                        user.attributes.get("mobile", ""),
                        user.attributes.get("email", ""),
                        user.attributes.get("special_path", ""),
                        user.attributes.get("shell", ""),
                        )
                file_lines.append(file_line.encode('utf8'))
        # Write each line to the password file.
        pwdfile = open("/tmp/passwdfile", "w")
        for line in file_lines:
            if len(line) > 0:
                pwdfile.write(line)
        pwdfile.close()
