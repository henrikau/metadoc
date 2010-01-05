import socket, os
from SocketServer import BaseServer
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from OpenSSL import SSL

class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass):
        BaseServer.__init__(self, server_address,  HandlerClass)
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        # Get key and certificate:
        ctx.use_privatekey_file('userkey.pem')
        ctx.use_certificate_file('usercert.pem')
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family, self.socket_type))
        self.server_bind()
        self.server_activate()

class SecureHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_header(200)

        self.wfile.write("<html><head><title>test</title></head><body>")
        self.print_form()
        self.wfile.write("</body></html>")

    def do_POST(self):
        global rootnode
        try:
            self.send_header(200)

            self.wfile.write("<html><head><title>test</title></head><body>")
            self.wfile.write("Got POST-data. How to retrieve?")
            self.print_form()
            self.wfile.write("<pre>\n")
            self.wfile.write("%s\n" %(self.headers))
            self.wfile.write("</pre>\n")
            self.wfile.write("</body></html>");

            return
            headers = self.headers.getHeader('content-type')
            print headers
            ctype, pdict = cgi.parse_header(self.headers.getHeader('content-type'))
            print ctype
            print pdict
            self.send_response('200')
            self.end_headers()
            self.wfile.write(ctype)
            self.wfile.write("<html><header><title>test</titel></header><body>")
            self.print_form()
            self.wfile.write("OK<br />%s" % (ctype))
            self.wfile.write("</body></html>")
            
        except:
            pass

    def send_headers(self, value):
        self.send_response(value)
        self.send_header('Content-Type:', 'text/html')
        self.end_headers()

    def print_form(self):
        self.wfile.write("<form action=\"\" method=\"POST\">\n")
        self.wfile.write("<input type=\"hidden\" name=\"meh\" value=\"2\" />\n")
        self.wfile.write("<input type=\"submit\" value=\"Submit\" />\n")
        self.wfile.write("</form>\n")

def test(HandlerClass = SecureHTTPRequestHandler,
         ServerClass = SecureHTTPServer):
    try:
        ServerClass(('', 8443), HandlerClass).serve_forever()
    except KeyboardInterrupt:
        print "Interrupt received. Shutting down."
        server.socket.close()

if __name__ == '__main__':
    test()
