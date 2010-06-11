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

from metaelement import MetaElement
import xml.etree.ElementTree

class Events(MetaElement):
    """
    Register Events and pack it in XML.
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

        param:
        date_up         : When it was up and fully operational
        reason          : The reason for coming back up (if changed from going down)
        remarks         : Any other remarks.
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

        param:
        reason          : The reason why the system is going down
        dateDown        : When it's going down
        dateUp          : When it's planned to be back online
        shareDown       : How large share of the system that will be down.
                          This value should be on integer-form and be in
                          percent-representation:
                          e.g. '90' means that 90% of the system will be down

                          It can be in either string, int or float

        remarks         : Any remarks
        """
        if type(shareDown).__name__ == "int":
            shareDown = "%d" % (shareDown)
        elif type(shareDown).__name__ == "float":
            shareDown = "%f" % (shareDown)

        entry = xml.etree.ElementTree.Element("resourceDown",
                                              reason=reason,
                                              dateDown=dateDown,
                                              dateUp=dateUp,
                                              shareDown=shareDown)
        if remarks:
            rem = xml.etree.ElementTree.SubElement(entry, "remarks")
            rem.text = remarks
        self.element.append(entry)
