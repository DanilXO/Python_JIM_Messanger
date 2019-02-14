# Программа сервера времени
import socket
import sys
from JIMProtocol import MessageBuilder

class Server:
    _server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создает сокет TCP
    connections = []

    def __init__(self, ip="localhost", port=8888):
        self._server_socket.bind((ip, port))  # Присваивает порт 8888
        self._server_socket.listen(5)  # Переходит в режим ожидания запросов;
        # одновременно обслуживает не более 5 запросов
        print('Server started...')

    def run(self):
        while True:
                client, addr = self._server_socket.accept()  # Принять запрос на соединение
                print("Получен запрос на соединение от %s" % str(addr))
                data = client.recv(1024)  # Принять не более 1024 байтов данных
                self.parse_message(client, data)

    def parse_message(self, client, msg):
        msg = msg.decode("ascii")
        print(msg)
        parsed_msg = MessageBuilder.get_object_of_json(msg)
        # parsed_msg = json.JSONDecoder(object_hook=MessageBuilder).decode(msg)
        if parsed_msg.action == "presence":
            self.send_responce(client, 200, "{} is currently present.".format(parsed_msg.user.name))

    def send_responce(self, client, code, alert=None):
        gen_response = MessageBuilder.create_response_message(code, alert)
        gen_response_json = gen_response.encode_to_json()
        client.send(gen_response_json.encode('ascii'))

if __name__ == '__main__':
    if (len(sys.argv))> 1:
        server = Server(str(sys.argv[1]), int(sys.argv[2]))
        server.run()
    else:
        server = Server()
        server.run()