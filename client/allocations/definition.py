#
#            Allocations.py is part of MetaDoc (Client).
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
from custom.updateallocations import UpdateAllocations
from allocations.entries import AllocationEntry

class Allocations(metaelement.MetaElement):
    """
    Allocations - the granted resources for a project.
    """
    xml_tag_name = "allocations"
    update_handler = UpdateAllocations

    def __init__(self):
        """
        init()
        """
        super(Allocations, self).__init__(Allocations.xml_tag_name)
        self.legal_element_types = (AllocationEntry,)
