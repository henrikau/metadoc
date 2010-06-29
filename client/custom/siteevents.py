# -*- coding: utf-8 -*-
#
#            custom/siteevents.py is part of MetaDoc (Client).
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
from abstract import MetaOutput
from events.entries import ResourceUpEntry, ResourceDownEntry
import utils

class SiteEvents(MetaOutput):
    def populate(self):
        """Function to populate `self.items` with ResourceUpEntry and 
        ResourceDownEntry.

        ResourceUpEntry takes the arguments dateUp, reason and remarks.
        Only dateUp is required. 

        ResourceDownEntry takes the arguments reason, dateDown, dateUp, 
        shareDown and remarks.
        Only remarks is optional. 

        Dates should be date, datetime or a RFC3339 string.

        """
        pass
