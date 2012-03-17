import threading
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import signal
import os
import glob
import cgi
import cgitb
cgitb.enable()

import constants
qryPath = os.path.abspath("../"+constants.logBasePath) + "/"



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

        self.send_response(200)

        req = self.getRequest()
        res = []
        res.extend(self.getList())
        res.append("<br/><hr><br/>")

        if len(req) == 0:
            self.printRes(res)
        else:
            self.printRes(res)

    def printRes(self, res):
        self.wfile.write(self.getHeader())
        self.end_headers()
        for line in res:
            self.wfile.write(line)
            print line

        self.wfile.write(self.getTail()  )


    def getRequest(self):
        # Parse the form data posted
        form = cgi.FieldStorage()
        print "FORM "+ str(form)
        req = {}

        if form.has_key("runName"):
            print "  RUN NAME PRESENT"
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
        #print "dirs" + str(dirs)

        res = []
        if len(dirs) == 0:
            return res

        lastDir = dirs[-1]
        #print "  lastdir " + lastDir

        res.append("<form id=\"runName\"><select>")
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

        res.append("</select>")
        res.append("<input type=\"submit\" method=\"get\" value=\"ok\"></input></form>")
        return res


    def getAllPaths(self):
        dirs = []
        #print "base " + constants.logBasePath

        list = os.listdir(qryPath)
        list.sort()

        if list is not None:
            for infile in list:
                #print "infile " + infile
                if os.path.isdir(qryPath + infile):
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

