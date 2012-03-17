import threading
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import signal
import os
import glob
import cgi
import cgitb
cgitb.enable()

import constants




class jobServer(BaseHTTPRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def do_GET(self):
        # self.request is the TCP socket connected to the client
        #self.data = self.request.recv(1024).strip()
        #print "{} wrote:".format(self.client_address[0])
        #print self.data
        # just send back the same data, but upper-cased
        req = self.getRequest()
        res = []
        res.extend(self.getList())

        if len(req) == 0:
            self.printRes(res)
        else:
            self.printRes(res)

    def printRes(self, res):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self.getHeader())

        for line in res:
            self.wfile.write(line)
            print line

        self.wfile.write(self.getTail()  )


    def getRequest(self):
        # Parse the form data posted
        form = cgi.FieldStorage()
        req = {}

        if "runName" not in form:
            return req
        else:
            # Echo back information about what was posted in the form
            for field in form.keys():
                field_item = form[field]
                if field_item.filename:
                    pass
                else:
                    # Regular form value
                    req[field] = form[field].value

        return req

    def getList(self):
        dirs = self.getAllPaths()
        res = []
        if len(dirs) == 0:
            return res

        lastDir = dirs[-1]

        res.append("<select>\n")
        #<select>
        #  <option value="volvo">Volvo</option>
        #  <option value="saab">Saab</option>
        #  <option value="mercedes">Mercedes</option>
        #  <option value="audi">Audi</option>
        #</select>

        for dir in dirs:
            if dir == lastDir:
                selected = " selected=\"yes\""
            else:
                selected = ""
            res.append("<option value=\""+dir+"\""+selected+">"+dir+"</option>")

        res.append("</select>\n")


    def getAllPaths(self):
        dirs = []
        #print "base " + constants.logBasePath

        list = os.listdir(os.path.abspath("../"+constants.logBasePath))
        list.sort()

        if list is not None:
            for infile in list:
                #print "infile " + infile
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
        return header


    def getTail(self):
        tail = \
        """
    </body>
</html>
        """
        return tail


class serverDaemon(threading.Thread):
    def __init__(self):
        super(serverDaemon, self).__init__()
        self.HOST, self.PORT = "localhost", 9999

        # Create the server, binding to localhost on port 9999
        serverInst      = HTTPServer((self.HOST, self.PORT), jobServer)
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
    #print "including finishing it"
    #daemon.stop()
    #daemon.join()
    #print "finished"

