# -*- coding: utf-8 -*-
#
#            Events.py is part of MetaDoc (Client).
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

from MetaElement import MetaElement
import xml.etree.ElementTree

class Events(MetaElement):
    """
    Register Events and pack it in XMl.
    """
    def __init__(self, host):
        MetaElement.__init__(self, "events")
        self.host = host
        self.element = xml.etree.ElementTree.Element(self.getName(), name=self.host)

    def addEntry(self):
        print "Events::addEntry(): NA,  use addUp() or addDown() instead."
        pass

    def addUp(self, date_up, reason=None, remarks=None):
        """
        addUp - notification about a system bein back up again.
        """
        entry = xml.etree.ElementTree.Element("resourceUp",
                                              dateUp=date_up)
        if reason:
            entry.set('reason', reason)
        if remarks:
            rem = xml.etree.ElementTree.SubElement(entry, "remarks")
            rem.text = remarks
        self.element.append(entry)

    def addDown(self, reason, dateDown, dateUp, shareDown, remarks=None):
        """
        addDown() add notice about a planned (or not so planned) downtime.
        """
        entry = xml.etree.ElementTree.Element("resourceDown",
                                              reason=reason,
                                              dateDown=dateDown,
                                              dateUp=dateUp,
                                              shareDown=shareDown)
        if remarks:
            rem = xml.etree.ElementTree.SubElement(entry, "remarks")
            rem.text = remarks
        self.element.append(entry)
