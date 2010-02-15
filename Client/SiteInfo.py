# -*- coding: utf-8 -*-
#
#            SiteInfo.py is part of MetaDoc (Client).
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

class SiteInfo(MetaElement):
    """
    Register site-info and pack it in XMl.
    """
    def __init__(self, host):
        MetaElement.__init__(self, "siteInfo")
        self.host         = host
        self.element      = xml.etree.ElementTree.Element(self.getName(), name=self.host)
        self.legalElement = ['cores', 'nodes', 'totalDisk', 'usedDisk',
                             'totalSwap', 'usedSwap', 'totalMemory',
                             'usedMemory']
        self.legalMetric  = ['count', 'MB', 'GB', 'TB']

    def addEntry(self):
        print "SiteInfo::addEntry(): NA, use addSW() or addConfig() instead."
        pass

    def addSW(self, progName, version, license=None, infoURL=None):
        entry = xml.etree.ElementTree.Element("software", progName=progName, version=version)
        if license:
            entry.set('license', license)
        if infoURL:
            entry.set('infoURL', infoURL)
        self.element.append(entry)

    def addConfig(self, element, metric, volume):
        if not element in self.legalElement:
            print "Illegal element \"%s\" for site %s. Use one of %s" % (element, self.host, self.legalElement)
            return
        if not metric in self.legalMetric:
            print "Illegal metric \"%s\" for %s. Use one of %s" % (metric, self.host, self.legalMetric)
            return

        entry = xml.etree.ElementTree.Element("config",
                                              element=element,
                                              metric=metric,
                                              volume=volume)
        self.element.append(entry)
