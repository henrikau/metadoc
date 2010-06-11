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
    """
    Registers events and packs to XML. 

    Specifies cleaning methods for attributes to make sure they conform with 
    expected values. 
    """
    def __init__(self, *args, **kwargs):
        """
        Initialites the MetaElement and specifies legal values for attributes.
        """
        super(Configuration, self).__init__("config")
        self.element = xml.etree.ElementTree.Element(self.getName())
        self.legal_metric = ('count', 'MB', 'GB', 'TB')
        self.legal_element = ('cores','nodes','totalDisk',
                                'usedDisk','totalSwap','usedSwap',
                                 'totalMemory','usedMemory')
        self.legal_entrytypes = ('config_entry')
        self.entry_attribs = (
                                {'name':'element', 'cleanFunction':'cleanElement', 'required':True},
                                {'name':'metric', 'cleanFunction':'cleanMetric', 'required':True},
                                {'name':'volume', 'cleanFunction':'cleanVolume', 'required':True},
                            )


    def cleanElement(self, element):
        """Checks that the element attribute contains an allowed value"""
        if not element in self.legal_element:
            raise metaelement.IllegalAttributeValueError("element", element, self.legal_element, "Configuration")
        return element
    def cleanMetric(self, metric):
        """Checks that the metric attribute contains an allowed value"""
        if not metric in self.legal_metric:
            raise metaelement.IllegalAttributeValueError("metric", metric, self.legal_metric, "Configuration")
        return metric
    def cleanVolume(self, volume):
        """Converts volume to string if integer, and checks that the passed 
        variable is either string or int.

        Allows for unicode strings.
        """
        if isinstance(volume, int):
            volume = "%d" % (volume)
        if not isinstance(volume, basestring):
            raise metaelement.IllegalAttributeTypeError("volume", type(volume), "Configuration", ['str', 'int'])
        return volume

    def addEntry(self, entry_type, *args, **kwargs):
        """
        Add a configuration entry to the site's configuration.

        param:
        element         : The element described (nodes, cores, totalDisk, etc)
        metric          : The metric used to measure element (count, MB, GB, TB)
        volume          : Number of <metric> for the element described. Can be int or str.
        """
        if not entryType in entryTypes:
            raise metaelement.IllegalEntryTypeError(entryType, self.entryTypes)
        # FIXME - Verbose mode gives a message if more kwargs than entry_attribs allows.
        attribute_list = self.checkEntries(*args, **kwargs)
        entry = xml.etree.ElementTree.Element(entry_type,
                                                attribute_list)
        self.element.append(entry)
