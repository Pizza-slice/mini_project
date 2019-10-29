import json
import socket


class Client:
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 1902
        self.auth_code = ""

    def create_connection(self):
        client_socket = socket.socket()
        client_socket.connect((self.ip, self.port))
        return client_socket

    def log_in(self, username, password):
        data = {"type": "log-in", "username": username, "password": password}
        client_socket = self.create_connection()
        self.send_data_to_server(client_socket, json.dumps(data))
        data_from_srerver = json.loads(self.get_data_from_server(client_socket)) # todo check input
        if data_from_srerver["type"] == "failed":
            self.kill_connection(client_socket)
            return False, data_from_srerver["massage"]
        else:
            self.kill_connection(client_socket)
            self.auth_code = data_from_srerver["auth_code"]
            return True, None

    def create_user(self, username, password):
        data = {"type": "sign-in", "username": username, "password": password}
        client_socket = self.create_connection()
        self.send_data_to_server(client_socket, json.dumps(data))
        data_from_srerver = json.loads(self.get_data_from_server(client_socket))
        if data_from_srerver["type"] == "failed":
            self.kill_connection(client_socket)
            return False, data_from_srerver["massage"]
        else:
            self.kill_connection(client_socket)
            return True, None

    @staticmethod
    def kill_connection(client_socket):
        client_socket.close()

    @staticmethod
    def send_data_to_server(client_socket, data):
        client_socket.send(data.encode())

    @staticmethod
    def get_data_from_server(client_socket):
        return client_socket.recv(1024).decode()
