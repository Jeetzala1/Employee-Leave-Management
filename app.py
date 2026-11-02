from http.server import BaseHTTPRequestHandler, HTTPServer


class LeaveApp(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            b"<h1>Employee Leave Management</h1>"
            b"<p>Application is running successfully!</p>"
        )


server = HTTPServer(("0.0.0.0", 5000), LeaveApp)
print("Leave Management App running on port 5000", flush=True)
server.serve_forever()
