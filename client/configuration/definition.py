#
#            configuration.py is part of MetaDoc (Client).
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
from custom.siteconfiguration import SiteConfiguration
from configuration.entries import ConfigEntry

class Configuration(metaelement.MetaElement):
    """ Registers events and packs to XML. 

    Specifies cleaning methods for attributes to make sure they conform with 
    expected values. 

    """
    xml_tag_name = "config"
    site_handler = SiteConfiguration

    def __init__(self):
        """ Initialites the MetaElement and specifies legal values for attributes. """
        super(Configuration, self).__init__(Configuration.xml_tag_name)
        self.legal_element_types = (ConfigEntry,)
