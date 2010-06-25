# -*- coding: utf-8 -*-
#
#            custom/updateprojects.py is part of MetaDoc (Client).
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

from abstract import MetaInput

import datetime

class UpdateProjects(MetaInput):
    """ Class for processing recieved project data. """
    def process(self):
        """ Called when project data is parsed and should be processed for the 
        site. 

        `self.items` will contain a list of `projects.definition.Projects` 
        instances. These instances have defined `get_user_list()` that provides
        a list of users for the given project.

        See doc/examples/custom/updateprojects.py for example on creating a 
        project user file.

        """
        pass
