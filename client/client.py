import json
import socket


class Client:
    """
    the protocol is a json data that is have a "type" key that hold the action you want to do
    """
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 1902
        self.auth_code = ""

    def create_connection(self):
        """
        open a socket to the server
        my protocol is always open and closing sockets
        :return:
        """
        client_socket = socket.socket()
        client_socket.connect((self.ip, self.port))
        return client_socket

    def log_in(self, username, password):
        data = {"type": "log-in", "username": username, "password": password}
        client_socket = self.create_connection()
        self.send_data_to_server(client_socket, json.dumps(data))
        data_from_srerver = json.loads(self.get_data_from_server(client_socket))  # todo check input
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
            return True, data_from_srerver["massage"]

    def get_user_id_list(self):
        data = {"type": "get-id-list", "auth_code": self.auth_code}
        client_socket = self.create_connection()
        self.send_data_to_server(client_socket, json.dumps(data))
        data_from_server = json.loads(self.get_data_from_server(client_socket))
        if data_from_server["type"] == "success":
            self.kill_connection(client_socket)
            return data_from_server["data"]
        else:
            print(data_from_server["error_massage"])

    def get_username_from_id(self, user_id):
        data = {"type": "get-username-from-id", "auth_code": self.auth_code, "user_id": user_id}
        client_socket = self.create_connection()
        self.send_data_to_server(client_socket, json.dumps(data))
        temp = self.get_data_from_server(client_socket)
        data_from_server = json.loads(temp)
        if data_from_server["type"] == "success":
            self.kill_connection(client_socket)
            return data_from_server["data"]
        else:
            print(data_from_server["error_massage"])

    def get_massages_from_server(self):
        data = {"type": "get-massages", "auth_code": self.auth_code}
        client_socket = self.create_connection()
        self.send_data_to_server(client_socket, json.dumps(data))
        data_from_server = json.loads(self.get_data_from_server(client_socket))
        return data_from_server

    def send_massage(self, massage, send_to="all"):
        data = {"type": "send-massage", "auth_code": self.auth_code, "to": send_to, "data": massage}
        client_socket = self.create_connection()
        self.send_data_to_server(client_socket, json.dumps(data))
        data_from_server = json.loads(self.get_data_from_server(client_socket))
        if data_from_server["type"] == "failed":
            print(data_from_server["error_massage"])

    @staticmethod
    def kill_connection(client_socket):
        client_socket.close()

    @staticmethod
    def send_data_to_server(client_socket, data):
        client_socket.send(data.encode())

    @staticmethod
    def get_data_from_server(client_socket):
        return client_socket.recv(1024).decode()
