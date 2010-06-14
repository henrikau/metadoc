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
from datetime import datetime, timedelta

from abstract import MetaOutput
from events.entries import ResourceUpEntry, ResourceDownEntry
#### Testing Purposes ####
import random
#### Testing Purposes end ####

class SiteEvents(MetaOutput):
    def populate(self):
        """
        Function to populate self.items with ConfigItem
        """
        for i in xrange(5):
            t = random.randint(0,1)
            if t == 0:
                self.items.append(ResourceDownEntry('Testing purposes', datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), (datetime.now()+timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S"), 95.5))
            else:
                self.items.append(ResourceUpEntry(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), 'We are BACK!', 'We were down'))
