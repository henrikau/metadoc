"""
XML_Client. Simple client for pushing XML over HTTPS
"""
#!/usr/bin/env python
# The HTTPSClientAuthHandler is inspired by
#       http://www.threepillarsoftware.com/soap_client_auth
#
import urllib, urllib2, httplib

class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
    """
    HTTPSClientAuthHandler extends HTTPSHandler

    Client code for a http-handler capable of SSL and X.509 authN
    """
    def __init__(self, key, cert):
        """
        Init HTTPSClientAuthHandler
        key: the private key
        cert: the certificate

        both to use with the AuthN/AuthZ
        """
        urllib2.HTTPSHandler.__init__(self)
        self.key  = key
        self.cert = cert

    def https_open(self, req):
        """
        Open the connection.
        """
        return self.do_open(self.getConncetion, req)

    def getConncetion(self, host, timeout=300):
        """
        Get the connection.
        """
        return httplib.HTTPSConnection(host, key_file=self.key,
                                       cert_file=self.cert)


class XML_Client:
    """
    Send XML over HTTPS + X.509 authN channel
    """
    def __init__(self, addr, key, cert):
        """
        XML_Client()

        addr: the address we are going to send data to
        key, cert: keypair to use for authentication.

        The client will connect to the site via HTTPS and use the
        provided keypair for authentication.

        If the host is down or the port/protocol is wrong, it will fail
        pretty hard. No logic to handle this has been added yet.
        """
        self.https_client = HTTPSClientAuthHandler(key, cert)
        self.url          = addr

    def send(self, xml_data):
        """
        Send XML-data to the host.

        param:
        xml_data: The data to send to the site.

        The result is returned raw without parsing it.

        """
        post    = { 'metadoc' : xml_data }
        data    = urllib.urlencode(post)
        opener  = urllib2.build_opener(self.https_client)
        return opener.open(self.url, data)

