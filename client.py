# Программа клиента, запрашивающего текущее время
import json
import socket
import sys
from JIMProtocol import MessageBuilder, JSONMessageEncoder

class Client:
    _client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self, server_address='localhost', port=8888):
        self._client_socket.connect((server_address, port))  # Соединиться с сервером
        self.login = None

    def run(self):
        self.sendMsg("presence")
        response = None
        while response is None:
            response = self._client_socket.recv(1024)
            self.parse_response(response)

    def parse_response(self, response):
        response = response.decode("ascii")
        print(response)
        parsed_response = JSONMessageEncoder().message_decode(response)
        print(parsed_response.response)
        print(parsed_response.alert)

    def sendMsg(self, type="presence"):
        if self.login is None:
            self.login = input("Login:")
        gen_message = MessageBuilder.create_presence_message(self.login)
        # gen_message_json = JSONMessageEncoder().encode(gen_message)
        # print(gen_message)print(gen_message)
        gen_message_json = JSONMessageEncoder().encode(gen_message)
        self._client_socket.send(gen_message_json.encode('ascii'))

    def __del__(self):
        self._client_socket.close()

if __name__ =='__main__':
    if (len(sys.argv)) == 2:
        client = Client(str(sys.argv[1]), int(sys.argv[2]))
        client.run()
    else:
        client = Client()
        client.run()
