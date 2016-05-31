import SimpleHTTPServer
import BaseHTTPServer
import SocketServer

PORT = 8888

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
   def do_HEAD(s):
      s.send_response(200)
      s.send_header("Content-type", "application/json; charset=utf-8")
      s.end_headers()
   def do_GET(s):
      """Respond to a GET request."""
      s.send_response(200)
      s.send_header("Content-type", "application/json; charset=utf-8")
      s.end_headers()
      s.wfile.write("<html><head><title>Title goes here.</title></head>")
      s.wfile.write("<body><p>This is a test.</p>")
      s.wfile.write(s.path)
   def do_POST(s):
      s.send_response(200)
      s.send_header("Content-type", "application/json; charset=utf-8")
      s.end_headers()

#httpd = SocketServer.TCPServer(("", PORT), Handler)
httpd = SocketServer.TCPServer(("", PORT), MyHandler)


print "serving at port", PORT
httpd.serve_forever()
