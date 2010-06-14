# -*- coding: utf-8 -*-
#
#            custom/abstract.py is part of MetaDoc (Client).
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

"""
Abstract classes for site specific parsing of input and output data.
"""

class MetaOutput:
    """ Abstract class defining an interface for sending information from the
    site to the server. 

    """
    def __init__(self):
        """ Creates self.items that should be populated with MetaElement 
        sub-classes that should be sent to the server. 

        """
        self.items = []
    def populate(self):
        """ populate : Populates self.items
        
        Has to be populated in the inherited class.

        """
        raise Exception("populate has not been implemented, and function cannot be used!")
    def fetch(self):
        """ Returns a list of items to be sent. """
        return self.items

class MetaInput:
    """ Abstract class defining an interface for processing recieved data
    from the server.

    """
    def __init__(self, items):
        """ Creates self.items populated with MetaElement sub-classes 
        recieved from the server. 

        """
        self.items = items

    def process(self):
        """ process : Processes self.items

        Has to be created in the inherited class.

        """
        raise Exception("process has not been implemented, and function cannot be used!")
