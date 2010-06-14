# -*- coding: utf-8 -*-
#
#            custom/sitesoftware.py is part of MetaDoc (Client).
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
from software.entries import SoftwareEntry
#### Testing Purposes ####
import random
#### Testing Purposes end ####

class SiteSoftware(MetaOutput):
    def populate(self):
        """ Function to populate self.items with SoftwareEntry.

        Customize this function to fit to your site.

        """
        for i in xrange(5):
            self.items.append(SoftwareEntry('GCC', '%d.%d.%d' % (random.randint(0,10), random.randint(0,10), random.randint(0,10)), "GPLv2", "http://gcc.no"))
