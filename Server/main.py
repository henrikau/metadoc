#!/usr/bin/env python
from OpenSSL import crypto
from Config import Config

# Get certificate and key
# cert = crypto.load_certificate(crypto.FILETYPE_PEM, open('usercert.pem').read())
# key  =  crypto.load_privatekey(crypto.FILETYPE_PEM, open('userkey.pem').read())
# print cert.get_subject()
# print cert.get_issuer()
# print key.type()
# print key.bits()

config = Config()
counter = int(config.get('counter'))
if not counter:
    counter = 0

counter = counter + 1
config.set('counter', counter)

print "used counter %d times" % (counter)
