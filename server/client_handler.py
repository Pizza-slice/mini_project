import json
import threading

import database


class ClientHandler(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket

    def get_data_from_client(self):
        return self.client_socket.recv(1024).decode()

    def send_data_to_client(self, data):
        self.client_socket.send(data)

    def run(self):
        data = self.get_data_from_client()
        json_data = json.loads(data)  # todo check data input
        if json_data["type"] == "log-in":
            account_database = database.AsycDatabase("database.db")
            success, massage = account_database.check_user(json_data["username"], json_data["password"])
            if not success:
                self.send_data_to_client(json.dumps({"type": "failed", "massage": massage}).encode())
            else:
                auth_code = account_database.get_auth_code(json_data["username"])
                self.send_data_to_client(json.dumps({"type": "success", "auth_code": auth_code}).encode())
        if json_data["type"] == "sign-in":
            account_database = database.AsycDatabase("database.db")
            success, massage = account_database.create_user(json_data["username"], json_data["password"])
            if not success:
                self.send_data_to_client(json.dumps({"type": "failed", "massage": massage}).encode())
            else:
                self.send_data_to_client(json.dumps({"type": "success", "massage": massage}).encode())


def main():
    pass


if __name__ == '__main__':
    main()
