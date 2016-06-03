import SimpleHTTPServer
import BaseHTTPServer
import SocketServer
import cgi
import logging
import sys
import json
from createQuery import *

#sys.stdout = open('logs.txt', 'w')
#sys.stderr = open('logs.txt', 'w')

def toJSON(cur):
    json_string = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    return json.dumps(json_string)

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
        
        isUser = checkUser(postvars['username'][0], postvars['passHash'][0])
        print isUser
        
        if method == "login":
            validUsername = checkUsername(postvars['username'][0])
            if isUser: # is a user
                json = '{"status" : 0}'
            elif not validUsername: #is not a user but can create account
                json = '{"status" : 1}'
            else: #wrong password/username already taken
                json = '{"status" : 2}'
        elif method == "addUser":
            json = ""
            addUser(postvars)
        elif not isUser: #Dont allow other function calls unless valid user
            json = '{"status" : "failure"}'
        elif method == "addNote":
            json = ""
            print "ADDNOTE"
            addNote(postvars)
        elif method == "modifyNote":
            json = ""
            modifyNote(postvars)
        elif method == "deleteNote":
            json = ""
            deleteNote(postvars)
        elif method == "getNotes":
            print "GETNOTES"
            json = toJSON(getNotes(postvars))
        elif method == "getNote":
            json = toJSON(getNote(postvars))
        elif method == "search":
            json = toJSON(search(postvars))
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
