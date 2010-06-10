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
from MetaElement import MetaElement
import xml.etree.ElementTree

class Allocations(MetaElement):
    """
    Allocations - the granted resources for a project.
    """
    def __init__(self):
        """
        init()
        """
        MetaElement.__init__(self, "allocations")
        self.element = xml.etree.ElementTree.Element(self.getName())
        self.legalClass = ["pri", "nonpri"]

    def addEntry(self, account_nmb, hours, all_class, period):
        """
        add an allocation-entry to the list of allocations.

        param:
        account_nmb     : the account-identifier (e.g. 'NN12345')
        hours           : the number of hours to log. Can be either String or int
        all_class       : Allocation class ('pri' or 'nonpri')
        period          : The period (e.g. '2010.1')
        """
        if not all_class in self.legalClass:
            print "Illegal class \"%s\" for Allocations (%s). Use one of %s." % (all_class, account_nmb, self.legalClass)
            return
        if type(hours).__name__ == 'int':
            hours = "%d" % (hours)
        entry = xml.etree.ElementTree.Element("all_entry",
                                              account_nmb=account_nmb,
                                              hours=hours,
                                              all_class=all_class,
                                              period=period)
        self.element.append(entry)
