from my_webserver import MyWebServer
from http.server import SimpleHTTPRequestHandler

class ManuseioHttpRequest(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<html><body><h1>Olá Mundo!</h1></body></html>".encode())

        else:
            self.send_error(404)

app = MyWebServer(ManuseioHttpRequest)

if __name__ == "__main__":
    app.run()