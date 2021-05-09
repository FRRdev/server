import os, sys
from http.server import HTTPServer, CGIHTTPRequestHandler

webdir = '.'  # a directory with HTML files and a cgi-bin subdirectory for scripts
port = 8000

if len(sys.argv) > 1: webdir = sys.argv[1]
if len(sys.argv) > 2: port = int(sys.argv[2])
print('webdir "%s", port %s' % (webdir, port))

os.chdir(webdir)  # go to the web root directory
srvraddr = ('', port)
srvrobj = HTTPServer(srvraddr, CGIHTTPRequestHandler)
srvrobj.serve_forever()
