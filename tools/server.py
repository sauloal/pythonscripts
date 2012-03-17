import SocketServer
import threading
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import signal
import os

import constants
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
        self.wfile.write(self.getHeader())
        self.wfile.write(self.getTail()  )

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


class serverDaemon(threading.Thread):
    def __init__(self):
        super(serverDaemon, self).__init__()
        self.HOST, self.PORT = "localhost", 9999

        # Create the server, binding to localhost on port 9999
        serverInst      = SocketServer.TCPServer((self.HOST, self.PORT), jobServer)
        self.serverInst = serverInst

    def run(self):
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print "running server"
        self.serverInst.serve_forever()
        print "i can do stuff me"

    def stop(self):
        #self.serverInst.close_request()
        #self.serverInst.finish_request()
        self.serverInst.server_close()
        self.serverInst.shutdown()


print "starting class"
daemon = serverDaemon()


def signal_handler(signal, frame):
    print '!'*50
    print "You've sent signal " + str(signal) + ". exiting"
    print '!'*50
    daemon.stop()
    daemon.join()
    print "finished"
    sys.exit(signal)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    print "starting daemon"
    daemon.start()
    print "daemon started"
    print "now i can run more stuff"
    print "including finishing it"
    #daemon.stop()
    #daemon.join()
    #print "finished"

