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
import datetime

from abstract import MetaInput

class UpdateUsers(MetaInput):
    """ Class for processing recieved user data. """
    def process(self):
        """ Called when user data is parsed and should be processed for the 
        site.

        `self.items` will contain a list of `users.definition.Users` elements, 
        where each element in it's sub_elements will be a 
        `users.entries.UserEntry`. 

        See doc/examples/custom/updateusers.py for example on creating a 
        shadow file from data.

        """
        pass
