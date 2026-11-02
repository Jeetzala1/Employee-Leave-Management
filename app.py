from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


VALID_EMPLOYEE_ID = "EMP001"
VALID_PASSWORD = "password123"


class LeaveApp(BaseHTTPRequestHandler):
    def _send_page(self, body: bytes, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        login_page = b"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Employee Portal Login</title></head>
<body>
  <h1>Employee Portal</h1>
  <form method="post">
    <label for="employee_id">Employee ID</label>
    <input id="employee_id" name="employee_id" type="text" required>
    <label for="password">Password</label>
    <input id="password" name="password" type="password" required>
    <button id="login_button" type="submit">Login</button>
  </form>
</body>
</html>"""
        if self.path == "/dashboard":
            dashboard = b"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Employee Dashboard</title></head>
<body><h1 id="welcome_message">Welcome, EMP001</h1></body></html>"""
            self._send_page(dashboard)
            return
        self._send_page(login_page)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        form = parse_qs(self.rfile.read(content_length).decode("utf-8"))
        employee_id = form.get("employee_id", [""])[0]
        password = form.get("password", [""])[0]

        if employee_id == VALID_EMPLOYEE_ID and password == VALID_PASSWORD:
            self.send_response(303)
            self.send_header("Location", "/dashboard")
            self.end_headers()
            return

        login_page = b"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Employee Portal Login</title></head>
<body>
  <h1>Employee Portal</h1>
  <p id="error_message" role="alert">Invalid employee ID or password.</p>
  <form method="post">
    <label for="employee_id">Employee ID</label>
    <input id="employee_id" name="employee_id" type="text" required>
    <label for="password">Password</label>
    <input id="password" name="password" type="password" required>
    <button id="login_button" type="submit">Login</button>
  </form>
</body>
</html>"""
        self._send_page(login_page, status=401)


server = HTTPServer(("0.0.0.0", 5000), LeaveApp)
print("Leave Management App running on port 5000", flush=True)
server.serve_forever()
