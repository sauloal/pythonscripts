#!/usr/bin/python
import threading
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import os
import glob
import re
import itertools
import socket
from urlparse import urlparse, parse_qs
import signal

import constants
qryPath      = os.path.abspath("../"+constants.logBasePath) + "/"
qryPath      = os.path.abspath(constants.logBasePath) + "/"
jobPrefix    = "jobLaunch"
textAreaCols = "80"
textAreaRows = "5"
HOST, PORT   = "localhost", 9999



def rblocks(f, blocksize=4096):
    """Read file as series of blocks from end of file to start.

    The data itself is in normal order, only the order of the blocks is reversed.
    ie. "hello world" -> ["ld","wor", "lo ", "hel"]
    Note that the file must be opened in binary mode.
    """
    if 'b' not in f.mode.lower():
        raise Exception("File must be opened using binary mode.")
    size = os.stat(f.name).st_size
    fullblocks, lastblock = divmod(size, blocksize)

    # The first(end of file) block will be short, since this leaves 
    # the rest aligned on a blocksize boundary.  This may be more 
    # efficient than having the last (first in file) block be short
    f.seek(-lastblock,2)
    yield f.read(lastblock)

    for i in range(fullblocks-1,-1, -1):
        f.seek(i * blocksize)
        yield f.read(blocksize)

def tail(f, nlines):
    buf = ''
    result = []
    for block in rblocks(f):
        buf = block + buf
        lines = buf.splitlines()

        # Return all lines except the first (since may be partial)
        if lines:
            result.extend(lines[1:]) # First line may not be complete
            if(len(result) >= nlines):
                return result[-nlines:]

            buf = lines[0]

    return ([buf]+result)[-nlines:]


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

    def do_PNG(s):
        s.send_response(200)
        s.send_header("Content-type", "image/png")
        s.end_headers()

    def do_GET(self):
        # self.request is the TCP socket connected to the client

        res           = []
        req           = self.getRequest()
        self.req      = req
        runNames      = req.get('runName', None)
        files         = req.get('file',    None)
        self.files    = files
        self.runNames = runNames
        if files is not None and len(files) > 0:
            self.file     = files[0]
        else:
            self.file     = None
            
        if runNames is not None and len(runNames) > 0:
            self.runName  = runNames[0]
        else:
            self.runName  = None

        if len(req) != 0 and self.runName is not None:
            self.returnRequestedData()
        else:
            res.extend(self.getForm())
            self.printRes(res)


        #2012_03_17_16_22_59_369930.png
        #2012_03_17_16_22_59_505476_f0.png
        #jobLaunch_f0.dump
        #jobLaunch_f0.err
        #jobLaunch_f0.out
        #jobLaunch.log
        #jobLaunch.out

    def returnRequestedData(self):
        res = []
        if self.file is not None:
            #print " FILE DEFINED"
            self.serveFile()
        else:
            #print " FILE NOT DEFINED"
            res.extend(self.getForm()     )
            if self.runName is not None:
                #print "   RUN NAME DEFINED"
                res.extend(self.serveContent())

            self.printRes(res)


    def serveFile(self):
        #print " SERVING FILE :: QRY PATH " + qryPath + " RUN NAME " + self.runName + " FILE " + self.file
        
        self.do_PNG()
        runPath = os.path.join(qryPath, self.runName, self.file)
        f = open(runPath)
        self.wfile.write(f.read())
        f.close()

    def serveContent(self):
        #print "RUN NAME "+str(self.runName)
        res = []
        if self.runName is None:
            return res

        res.append("<h1 style='margin: 0px'>RESPONSE TO " + self.runName + "</h1>")
        files     = self.getFilesInRun(     self.runName )
        byProgram = self.groupByProgram(    files        )

        index     = self.getIndexTable(     byProgram)
        images    = self.getImageFilesTable(byProgram)
        logs      = self.getLogFilesTable(  byProgram)

        res.extend(index )
        res.extend(images)
        res.extend(logs  )

        return res

    def getImageFilesTable(self, byProgram):
        res      = []
        pngDates = {}

        if len(byProgram.keys()) > 1:
            for prog in byProgram.keys():
                data   = byProgram[prog]
                if data.has_key('image'):
                    dates  = data['image']
                    for date in dates.keys():
                        data = dates[date]
                        pngDates[date] = prog

        datesNames   = pngDates.keys()
        datesNames.sort()
        lastDate     = datesNames[-1]
        lastProgName = pngDates[lastDate]
        images       = byProgram[lastProgName]
        dates        = images['image']
        data         = dates[lastDate]
        file         = data['file']
        res.append("<h3 style='margin: 0px'>"+lastProgName+" - "+lastDate+"</h3>")
        res.append("<img src=\"/?runName="+self.runName+"&file="+file+"\"/>")

        return res

    def getLogFilesTable(self, byProgram):
        res = []
        if len(byProgram.keys()) > 1:
            res.append("<table colwidth=1>")
            for prog in byProgram.keys():
                data = byProgram[prog]
                out  = data.get('out', None)
                err  = data.get('err', None)
                if ( prog == '' ):
                    prog = "Global"
                
                res.append("<tr>")
                res.append("<td colspan=\"2\">")
                res.append("<a name=\""+prog+"\"></a>")
                res.append("<h3 style='margin: 0px'>"+prog+"</h3>")
                res.append("</td>")
                res.append("</tr>")
                res.append("<tr>")
                
                res.append("<td><h7 style='margin: 0px'>Out</h7></td>")
                res.append("<td><h7 style='margin: 0px'>Err</h7></td>")
                res.append("</tr>")

                res.append("<tr>")
                res.append("<td>")                

                if out is not None:
                    res.extend(self.getFileContent(out))
                res.append("</td>")

                res.append("<td>")
                if err is not None:

                    res.extend(self.getFileContent(err))

                res.append("</td>")
                res.append("</tr>")
                
            res.append("</table>")
                
        return res

    def getIndexTable(self, byProgram):
        res = []
        res.append("<table>\n<tr>")
        maxCols = 5

        colCount = 0
        if len(byProgram.keys()) > 1:
            for prog in byProgram.keys():
                if prog == '':
                    continue
                colCount += 1
                res.append("<td><a href=\"#"+prog+"\">"+prog+"</a></td>")
                if ( colCount % maxCols ) == 0:
                    res.append("</tr><tr>")

        while ( colCount % maxCols ) != 0:
            res.append("<td></td>")
            colCount += 1

        res.append("</tr></table>")
        return res

    def getFileContent(self, fn):
        res = []

        res.append("<textarea name=\""+fn+"\" cols=\""+textAreaCols+"\" rows=\""+textAreaRows+"\">")
        #res.append("this box will contain the information from " + fn)
        
        fullFn = os.path.join(self.runPath, fn)
        #print "   OPENING " + fullFn
        
        f=open(fullFn,'rb')
        for line in tail(f, 20):
            res.append(line)
            #print line
        f.close
        
        res.append("</textarea>")
        return res

    def groupByProgram(self, files):
        res = {}
        if len(files) != 0:
            for file in files:
                #2012_03_17_16_22_59_369930.png
                #2012_03_17_16_22_59_505476_f0.png
                #              Y     Mo    D     H     Min   S     Ms
                m = re.search('((\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(\d+))_*(\S*?)\.png', file)
                if ( m is not None):
                    date      = m.group(1)
                    year      = m.group(2)
                    month     = m.group(3)
                    day       = m.group(4)
                    hour      = m.group(5)
                    min       = m.group(6)
                    sec       = m.group(7)
                    ms        = m.group(8)
                    program   = m.group(9)
                    #print "FILE " + file + " DATE "+ date +" YEAR " + year + \
                    #" MONTH " + month + " DAY " + day + " HOUR " + hour + \
                    #" MINUTE " + min + " SECOND " + sec + " MICROSECONDS " + ms +\
                    #"  PROGRAM '" + program

                    res[program] = {
                        'image': {
                            date: {
                                'file'     : file,
                                'date'     : (year, month, day, hour, min, sec, ms)
                            }
                        }
                    }
            


        if len(files) != 0:
            for file in files:
                #2012_03_17_16_22_59_369930.png
                #2012_03_17_16_22_59_505476_f0.png
                #              Y     Mo    D     H     Min   S     Ms
                m = re.search(jobPrefix+'(_*\S*?)\.(out|err|log)', file)
                if ( m is not None):
                    program = m.group(1)
                    ext     = m.group(2)

                    if program != '':
                        program   = program[1:]

                    if ext == 'log':
                        ext = 'err'

                    if res.has_key(program):
                        data      = res[program]
                        data[ext] = file
                    else:
                        res[program] = { ext: file }
        
        return res

    def getFilesInRun(self, runName):
        files = []
        #print "base " + constants.logBasePath

        runPath      = os.path.join(qryPath, runName)
        self.runPath = runPath
        list         = os.listdir(runPath)
        list.sort()

        if list is not None:
            for infile in list:
                #print "infile " + infile
                filePath = os.path.join(runPath, infile)
                if os.path.isfile(filePath):
                    files.append(infile)
        return files

    def printRes(self, res):

        self.do_HEAD()
        self.wfile.write(self.getHeader())

        for line in res:
            self.wfile.write(line + "\n")
            #print line

        self.wfile.write(self.getTail()  )


    def getRequest(self):
        # Parse the form data posted
        path  = self.path
        parse = urlparse(path)
        qry   = parse.query
        req   = parse_qs(qry)
        #print "REQUEST " + str(req)
        self.req = req

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
        self.getList()
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
            selected = ""
            if self.runName is not None:
                if dir == self.runName:
                    selected = " selected=\"yes\""
            else:
                if dir == lastDir:
                    selected = " selected=\"yes\""
            
            res.append("<option value=\""+dir+"\""+selected+">"+dir+"</option>")

        res.append("</select>")
        res.append("<input type=\"submit\" method=\"get\" value=\"ok\"></input></form>")
        res.append("<hr>")
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
    <head><META HTTP-EQUIV="refresh" CONTENT="15"></head>
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
    
    def log_message(self, format, *args):
        pass


class serverDaemon(threading.Thread):
    def __init__(self):
        super(serverDaemon, self).__init__()

        # Create the server, binding to localhost on port 9999
        
        #socket.error: [Errno 98] Address already in use
        try:
            serverInst      = HTTPServer((HOST, PORT), jobServer)
            self.serverInst = serverInst
        except socket.error, msg:
            self.serverInst = None
            pass

    def run(self):
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print "running server"
        if self.serverInst is not None:
            self.serverInst.serve_forever()
            print "i can do stuff me"
        else:
            print "skipping"

    def stopServer(self):
        print "STOPING SERVER"
        #self.serverInst.close_request()
        #self.serverInst.finish_request()
        if self.serverInst is not None:
            self.serverInst.server_close()
            self.serverInst.shutdown()
            
        print "STOPING THREAD"
        #self.stop()
        self.join()




print "starting class"
daemon = serverDaemon()

def signal_handler(signal, frame):
    print '!'*50
    print "You've sent signal " + str(signal) + ". exiting"
    print '!'*50
    daemon.stopServer()
    #daemon.stop()
    daemon.join()
    print "finished"
    sys.exit(signal)

signal.signal(signal.SIGINT, signal_handler)



if __name__ == "__main__":
    print "starting daemon"
    daemon.start()
    print "daemon started"
    print "check it at http://%s:%s?runName=%s" % (HOST, PORT, constants.timestamp)
    #print "including finishing it"
    #daemon.stop()
    #daemon.join()
    #print "finished"
