"""
HTTPS_Server

A simple server capable of handling SSL-connections and X.509 authenticated sessions.

modified version of:
http://code.activestate.com/recipes/442473/

"""
import socket, os, pprint
from SocketServer import BaseServer
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
from OpenSSL import SSL

class HTTPS_Server():
    """
    HTTPS_Server
    """
    def __init__(self, config):
        self.valid  = False

        self.config = config
        if not self.config:
            print "No config set, cannot continue."
            return

        self.addr   = self.config.get('server_address')
        if not self.addr:
            print "No server-address specified in config. Aborting"
            print "You need to set the variable 'server_address' in the config"
            return
        self.port   = self.config.getInteger('server_port')
        if not self.port:
            print "No server-port specified in config. Aborting"
            print "You need to set the variable 'server_port' in the config"
            return

        self.context = SSL.Context(SSL.SSLv23_METHOD)
        try:
            self.context.use_privatekey_file(self.config.get('server_key_path'))
            self.context.use_certificate_file(self.config.get('server_cert_path'))
        except SSL.Error as sslerror:
            print "Error with supplied parameters. Key and certificate malformed or non-existant"
            self.valid = False
            return

        self.server = SecureHTTPServer((self.addr, self.port),
                                       SecureHTTPRequestHandler,
                                       self.context)
        self.valid  = True

    def start(self):
        if self.valid:
            sa = self.server.socket.getsockname()
            print "Starting server %s:%s" % (sa[0], sa[1])
            try:
                self.server.serve_forever()
            except KeyboardInterrupt as ki:
                print ""
                pass
            finally:
                print "Closing down server .. ",
                self.server.socket.close()
                print "done!"

class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass, ctx):
        BaseServer.__init__(self, server_address, HandlerClass)
        # Get key and certificate:
        try:
            self.socket = SSL.Connection(ctx, socket.socket(self.address_family, self.socket_type))
            self.server_bind()
            self.server_activate()
        except SSL.Error as sslerror:
            self.valid = False
            print "Could not init server"

class SecureHTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    Request-handler for the SecureHTTPServer

    """
    # def __init__(self, request, client_address, server):
    #     SocketServer.BaseRequestHandler(request, client_address, server)
    #     print "new request created"

    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

        self.start = "<html>\n\t<header>\n\t\t<title>test</title>\n\t</header>\n\t<body>\n"
        self.end   = "\t</body>\n</html>\n"

        print self.connection
        print self.rfile
        print self.wfile

    def do_GET(self):
        """
        Handle all GET-requests submitted to the server.
        """
        self.send_response(200)
        self.wfile.write(self.start)
        self.wfile.write(self.end)

    def send_headers(self, value):
        self.send_response(value)
        self.send_header('Date: ', 'Tue, 05 Jan 2010 13:33:09 GMT')
        self.send_header('Vary: ', 'Accept-Encoding')
        self.send_header('Content-Length: ', '910')
        self.send_header('Connection: ', 'close')
        self.end_headers()
        
    def print_form(self):
        self.wfile.write("<form action=\"\" method=\"POST\">\n")
        self.wfile.write("<input type=\"hidden\" name=\"meh\" value=\"2\" />\n")
        self.wfile.write("<input type=\"submit\" value=\"Submit\" />\n")
        self.wfile.write("</form>\n")
