import threading
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import signal
import os
import glob
from urlparse import urlparse, parse_qs

import constants
qryPath = os.path.abspath("../"+constants.logBasePath) + "/"



class jobServer(BaseHTTPRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(self):
        # self.request is the TCP socket connected to the client

        self.do_HEAD()

        res = []
        self.getList()
        res.extend(self.getForm())

        req = self.getRequest()

        if len(req) == 0:
            self.printRes(res)
        else:
            res.extend( self.returnRequestedData(req) )

            self.printRes(res)



    def returnRequestedData(self, req):
        runName = req.get('runName', None)
        print "RUN NAME "+str(runName)
        res = []
        if runName is None:
            return res

        runName = runName[0]
        res.append("RESPONSE TO " + runName)


        return res

    def printRes(self, res):
        self.wfile.write(self.getHeader())

        for line in res:
            self.wfile.write(line)
            print line

        self.wfile.write(self.getTail()  )


    def getRequest(self):
        # Parse the form data posted
        path  = self.path
        parse = urlparse(path)
        qry   = parse.query
        req   = parse_qs(qry)
        print "REQUEST " + str(req)

        return req

    def getList(self):
        dirs = self.getAllPaths()
        #print "dirs" + str(dirs)

        if len(dirs) == 0:
            return

        lastDir = dirs[-1]
        #print "  lastdir " + lastDir

        self.lenDirs = len(dirs)
        self.dirs    = dirs
        self.lastDir = lastDir

    def getForm(self):
        res     = []
        dirs    = self.dirs
        lenDirs = self.lenDirs
        lastDir = self.lastDir

        if dirs is None or len(dirs) == 0:
            return res

        res.append("<form id=\"runName\"><select name=\"runName\">")
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
        res.append("<br/><hr><br/>")
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

