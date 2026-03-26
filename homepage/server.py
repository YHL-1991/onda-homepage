import http.server
import os
import sys

port = int(os.environ.get('PORT', 8080))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"Serving on port {port}")
http.server.test(HandlerClass=http.server.SimpleHTTPRequestHandler, port=port, bind="0.0.0.0")
