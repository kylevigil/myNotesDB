import SimpleHTTPServer
import BaseHTTPServer
import SocketServer
import cgi
import logging
from createQuery import *

PORT = 8888

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json; charset=utf-8")
        s.end_headers()
    #Use GET to retrieve info from database
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "application/json; charset=utf-8")
        s.end_headers()

          


        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body><p>This is a test.</p>")
        s.wfile.write(s.path)
    #Use post for anything that updates the database
    def do_POST(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json; charset=utf-8")
        s.end_headers()
        ctype, pdict = cgi.parse_header(s.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(s.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(s.headers['content-length'])
            postvars = cgi.parse_qs(s.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {} 
     

        method = postvars['method'][0]
        print method

        if method == "addNote":
            json = addNote(postvars)
        elif method == "addUser":
            print 'called addUser'
            json = addUser(postvars)
        elif method == "modifyNote":
            json = modifyNote(postvars)
        elif method == "deleteNote":
            json = deleteNote(postvars)
        elif method == "getNotes":
            json = getNotes(postvars)
        else:
            json = "{nothing: 'else'}"
      
        if len(postvars):
            i = 0
            for key in sorted(postvars):
                #Uncomment to check parameters being passed 
                print 'ARG[%d] %s=%s' % (i, key, postvars[key])
                i += 1

        s.wfile.write(json)

httpd = SocketServer.TCPServer(("", PORT), MyHandler)


print "serving at port", PORT
httpd.serve_forever()
