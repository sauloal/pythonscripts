import SocketServer
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


def start():
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    serverInst = SocketServer.TCPServer((HOST, PORT), jobServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    serverInst.serve_forever()


if __name__ == "__main__":
    start()

