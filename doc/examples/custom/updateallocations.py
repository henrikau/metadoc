# -*- coding: utf-8 -*-
#
#            custom/updateallocations.py is part of MetaDoc (Client).
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

from abstract import MetaInput

class UpdateAllocations(MetaInput):
    """ Class that processes recieved allocations from server. """
    def process(self):
        """ Called when allocation data is parsed and should be processed for 
        the site.

        `self.items` will contain a list of `users.definition.Allocations` 
        elements, where each element in it's sub_elements will be a 
        `users.entries.AllocationEntry`. 

        Example file that creates quota file from data.

        """
        project_allocations = {}
        for item in self.items:
            for alloc in item.sub_elements:
                account_nmb = alloc.attributes.get("account_nmb")
                if len(account_nmb) == 0:
                    continue
                if account_nmb not in project_allocations.keys():
                    project_allocations[account_nmb] = {'pri': 0, 'nonpri': 0}
                if alloc.attributes.get("metric").lower() == "hours":
                    project_allocations[account_nmb][alloc.attributes.get("all_class")] += int(alloc.attributes.get("volume"))
        allfile = open("/tmp/allfile", "w")
        allfile.write("# account  quota[cpusecs]  nonpri_quota[cpusecs]\n")
        for proj in project_allocations.keys():
            allfile.write("%s%20s%20s\n" % (proj.lower(), 
                project_allocations[proj]['pri']*60*60, 
                project_allocations[proj]['nonpri']*60*60))
        allfile.close()
