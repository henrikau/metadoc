# -*- coding: utf-8 -*-
#
#            entries.py is part of MetaDoc (Client).
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

import metaelement

class ResourceUpEntry(metaelement.MetaElement):
    """ Describes a resourceUp entry. """
    xml_tag_name = "resourceUp"

    def __init__(self, date_up, reason=None, remarks=None):
        """ Initializes the MetaElement and specifies legal values for attributes.

        Allows for RemarksEntry sub-elements.

        """
        self.attributes = {
            'dateUp': date_up,
        }
        if reason:
            self.attributes['reason'] = reason
        super(ResourceUpEntry, self).__init__(ResourceUpEntry.xml_tag_name, self.attributes)
        
        self.legal_element_types = (RemarksEntry,)

        if remarks:
            self.add_element(RemarksEntry(remarks))

    def clean_dateUp(self, dateUp):
        """ Makes sure the date is in the correct format """
        return dateUp

class ResourceDownEntry(metaelement.MetaElement):
    """ Describes a resourceDown entry. """
    xml_tag_name = "resourceDown"

    def __init__(self, reason, date_down, date_up, share_down, remarks=None):
        """ Initializes the MetaElement and specifies legal values for attributes.

        Allows for RemarksEntry sub-elements.

        """
        self.attributes = {
            'reason': reason,
            'dateDown': date_down,
            'dateUp': date_up,
            'shareDown': share_down,
        }
        super(ResourceDownEntry, self).__init__(ResourceDownEntry.xml_tag_name, self.attributes)

        self.legal_element_types = (RemarksEntry, )

        if remarks:
            self.add_element(RemarksEntry(remarks))
    def clean_shareDown(self, share_down):
        if isinstance(share_down, int):
            share_down = "%d" % share_down
        elif isinstance(share_down, float):
            share_down = "%f" % share_down
        return share_down

class RemarksEntry(metaelement.MetaElement):
    """ Describes a remarks entry. """
    xml_tag_name = "remarks"

    def __init__(self, content):
        """ Initializes the MetaElement.
        
        Remarks have no attributes, but contains PCDATA.

        """
        super(RemarksEntry, self).__init__(RemarksEntry.xml_tag_name)
        self.text = content
