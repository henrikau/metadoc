# -*- coding: utf-8 -*-
#
#            custom/updateallocations.py is part of MetaDoc (Client).
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

class UpdateAllocations(MetaInput):
    """ Class that processes recieved allocations from server. """
    def process(self):
        """ Called when allocation data is parsed and should be processed for 
        the site.

        `self.items` will contain a list of `users.definition.Allocations` 
        elements, where each element in it's sub_elements will be a 
        `users.entries.AllocationEntry`. 

        See doc/examples/custom/updateallocations.py for example on creating a 
        quota file from data.

        """
        pass
