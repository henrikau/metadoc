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
    def __init__(self,key,cert):
        urllib2.HTTPSHandler.__init__(self)
        self.key  = key
        self.cert = cert

    def https_open(self, req):
        return self.do_open(self.getConncetion ,req)

    def getConncetion(self,host,timeout=300):
        return httplib.HTTPSConnection(host,key_file=self.key, cert_file=self.cert)


class XML_Client:
    def __init__(self):
        self.https_client = HTTPSClientAuthHandler('userkey.pem', 'usercert.pem')
        self.url          = "https://januz.dyndns.org/confusa_robot/index.php"

    def get_list(self):
        self.data    = urllib.urlencode({ 'action' : 'cert_list' })
        return res

    def send_revoke_list(self, eppn_list):
        post = { 'action' : 'revoke_list' }
        self.data = urllib.urlencode(post)
        return self.execute()

    def execute(self):
        opener = urllib2.build_opener(self.https_client)
        return opener.open(self.url, self.data)

cli = XML_Client()
print cli.get_list().read(),

