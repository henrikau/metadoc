# -*- coding: utf-8 -*-
#
#            allocations/entries.py is part of MetaDoc (Client).
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

class AllocationEntry(metaelement.MetaElement):
    """ AllocationEntry - Allocation for specific projects. """
    xml_tag_name = "all_entry"

    def __init__(self, account_nmb, volume, metric, all_class, period):
        """ Defines attributes for all_entry XML elements. 
        
        param:
        account_nmb         : Account identifier
        volume              : Amount of <metric>
        metric              : Measurement of <volume>
        all_class           : Allocation class
        period              : Period of allocation
        
        """
        attributes = {
            'account_nmb': account_nmb,
            'volume': volume,
            'metric': metric,
            'all_class': all_class,
            'period': period,
        }
        self.legal_metric = ('hours', 'mb',)
        self.legal_all_class = ('pri', 'nonpri',)
        super(AllocationEntry, self).__init__(AllocationEntry.xml_tag_name, attributes)

    def clean_metric(self, metric):
        """ Checks for legal values of metric. """
        self._clean_allowed_values(metric, self.legal_metric, 'metric', self.xml_tag_name, False)
        return metric

    def clean_all_class(self, all_class):
        """ Checks for legal values of all_class. """
        self._clean_allowed_values(all_class, self.legal_all_class, 'all_class', self.xml_tag_name, False)
        return all_class
            
