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
import urllib, urllib2, httplib, ssl, socket
import sys, os
import ConfigParser

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
        SCRIPT_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
        conf = ConfigParser.ConfigParser()
        conf.read("%s/%s" % (SCRIPT_PATH, "metadoc.conf"))
        v = conf.items("MetaDoc")
        v = dict(v)
        ca_certs = v.get("ca_certs")
        return HTTPSAuthServerConnection(host, key_file=self.key,
                                       cert_file=self.cert,
                                       cert_reqs=ssl.CERT_REQUIRED,
                                       ca_certs=ca_certs)

class HTTPSAuthServerConnection(httplib.HTTPSConnection):
    """ HTTPSAuthServerConnection extends httplib.HTTPConnection.
    
    Code for enabling server certificate verification in an SSL tunnel.

    """
    def __init__(self, host, port=None, key_file=None, cert_file=None,
                strict=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                cert_reqs=ssl.CERT_NONE, ca_certs=None):
        httplib.HTTPConnection.__init__(self, host, port, strict, timeout)
        self.key_file = key_file
        self.cert_file = cert_file
        self.cert_reqs = cert_reqs
        self.ca_certs = ca_certs
    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        self.sock = ssl.wrap_socket(sock, keyfile=self.key_file, 
                                    certfile=self.cert_file, 
                                    cert_reqs=self.cert_reqs, 
                                    ca_certs=self.ca_certs)


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

