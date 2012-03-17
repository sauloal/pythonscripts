import SocketServer
import threading
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


import constants
import os
import glob



class jobServer(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.getHeader())
        self.request.sendall(self.getTail())
        self.request.sendall(self.data.upper())

    def getAllPaths(self):
        dirs = []
        for infile in glob.glob( os.path.join(constants.logBasePath, '*') ):
            if os.path.isdir(infile):
                dirs.append(infile)
        return dirs

    def getHeader(self):
        header = \
        """
<html>
    <head></head>
    <body>
        """
        print header
        return header


    def getTail(self):
        tail = \
        """
    </body>
</html>
        """
        print tail
        return tail


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("Hello World!")

class serverDaemon(threading.Thread):
    def __init__(self):
        super(serverDaemon, self).__init__()
        self.HOST, self.PORT = "localhost", 9999

        # Create the server, binding to localhost on port 9999
        self.serverInst = SocketServer.TCPServer((self.HOST, self.PORT), jobServer)

    def run(self):
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        self.serverInst.serve_forever()
        print "i can do stuff me"


#Thread(target=serve_on_port, args=[1111]).start()
#serve_on_port(2222)


if __name__ == "__main__":
    daemon = serverDaemon()
    daemon.start()

