#
#            Configuration.py is part of MetaDoc (Client).
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
import xml.etree.ElementTree

class Configuration(metaelement.MetaElement):
    def __init__(self, *args, **kwargs):
        super(Configuration, self).__init__("config")
        self.element = xml.etree.ElementTree.Element(self.getName())
        self.legalMetric = ['count', 'MB', 'GB', 'TB']
        self.legalElement = ['cores','nodes','totalDisk',
                                'usedDisk','totalSwap','usedSwap',
                                 'totalMemory','usedMemory']
        self.entryAttribs = (
                                {'name':'element', 'cleanFunction':'cleanElement', 'required':True},
                                {'name':'metric', 'cleanFunction':'cleanMetric', 'required':True},
                                {'name':'volume', 'cleanFunction':'cleanVolume', 'required':True},
                            )


    def cleanElement(self, element):
        if not element in self.legalElement:
            raise metaelement.IllegalAttributeValueError("element", element, self.legalElement, "Configuration")
        return element
    def cleanMetric(self, metric):
        if not metric in self.legalMetric:
            raise metaelement.IllegalAttributeValueError("metric", metric, self.legalMetric, "Configuration")
        return metric
    def cleanVolume(self, volume):
        if isinstance(volume, int):
            volume = "%d" % (volume)
        if not isinstance(volume, basestring):
            raise metaelement.IllegalAttributeTypeError("volume", type(volume), "Configuration", ['str', 'int'])
        return volume

    def addEntry(self, *args, **kwargs):
        """
        Add a configuration entry to the site's configuration.

        param:
        element         : The element described (nodes, cores, totalDisk, etc)
        metric          : The metric used to measure element (count, MB, GB, TB)
        volume          : Number of <metric> for the element described. Can be int or str.
        """
        # FIXME - Verbose mode gives a message if more kwargs than entryAttribs allows.
        attributeList = self.checkEntries(*args, **kwargs)
        entry = xml.etree.ElementTree.Element("config_entry",
                                                attributeList)
        self.element.append(entry)
