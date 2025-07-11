from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

# Настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


content_types = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
}


class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за
    обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        if self.path == '/':
            self.path = '/contacts.html'

        _, ext = os.path.splitext(self.path)

        try:
            with open(self.path[1:], "rb") as file:  # Убираем первый символ '/' из пути
                content = file.read()

            content_type = content_types.get(ext, 'application/octet-stream')

            # Отправка успешного ответа и заголовков
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()

            self.wfile.write(content)

        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(f"<html><body><h1>500 Internal Server Error</h1><p>{str(e)}</p></body></html>", "utf-8"))

    def do_POST(self):
        """ Метод для обработки входящих POST-запросов """
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        print("Received POST data:", post_data.decode('utf-8'))

        try:
            json_data = json.loads(post_data)
            print("Parsed JSON data:", json_data)
        except json.JSONDecodeError:
            print("Failed to parse JSON data")

        # Отправляем ответ клиенту
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "Data received"}
        self.wfile.write(bytes(json.dumps(response), "utf-8"))

if __name__ == "__main__":
    # Инициализация веб-сервера
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started at http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    # Остановка веб-сервера
    webServer.server_close()
    print("Server stopped.")
