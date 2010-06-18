# -*- coding: utf-8 -*-
#
#            metahttp.py is part of MetaDoc (Client).
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
#
#!/usr/bin/env python
# The HTTPSClientAuthHandler is inspired by
#       http://www.threepillarsoftware.com/soap_client_auth
#
import urllib, urllib2, httplib

""" Simple client for pushing XML over HTTPS. """
class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
    """ HTTPSClientAuthHandler extends HTTPSHandler

    Client code for a http-handler capable of SSL and X.509 authN

    """
    def __init__(self, key, cert):
        """ Init HTTPSClientAuthHandler
        key: the private key
        cert: the certificate

        both to use with the AuthN/AuthZ

        """
        urllib2.HTTPSHandler.__init__(self)
        self.key  = key
        self.cert = cert

    def https_open(self, req):
        """ Open the connection. """
        return self.do_open(self.get_conncetion, req)

    def get_conncetion(self, host, timeout=300):
        """ Get the connection. """
        return httplib.HTTPSConnection(host, key_file=self.key,
                                       cert_file=self.cert)


class XMLClient:
    """ Send XML over HTTPS + X.509 authN channel. """
    def __init__(self, addr, key, cert):
        """ XMLClient()

        addr: the address we are going to send data to
        key, cert: keypair to use for authentication.

        The client will connect to the site via HTTPS and use the
        provided keypair for authentication.

        If the host is down or the port/protocol is wrong, it will fail
        pretty hard. No logic to handle this has been added yet.

        """
        self.https_client = HTTPSClientAuthHandler(key, cert)
        self.url = addr

    def send(self, xml_data = None):
        """ Send XML-data to the host.

        param:
        xml_data: The data to send to the site.

        The result is returned raw without parsing it.

        """
        opener = urllib2.build_opener(self.https_client)
        if xml_data:
            post = {'metadoc' : xml_data}
            data = urllib.urlencode(post)
            return opener.open(self.url, data)
        else:
            return opener.open(self.url)

