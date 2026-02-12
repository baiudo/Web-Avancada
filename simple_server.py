from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message = "<html><body><h1>Olá Mundo!</h1></body></html>"
        self.wfile.write(message.encode())

if __name__ == "__main__":
    server_adress = ('', 8000)
    httpd = HTTPServer(server_adress, MyHandler)
    print("Servidor rodando em http://localhost:8000")
    httpd.serve_forever()