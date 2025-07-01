from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети

class MyServer(BaseHTTPRequestHandler):
    """
    Специальный класс, который отвечает за
    обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open("contacts.html", "r", encoding="utf-8") as file:
            content = file.read()

        self.wfile.write(bytes(content, "utf-8"))

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
