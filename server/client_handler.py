import threading
import database
import json


class ClientHandler(threading.Thread):
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.database = database.AsycDatabase("database.db")

    def get_data_from_client(self):
        return self.client_socket.recv(1024).decode()

    def send_data_to_client(self, data):
        self.client_socket.send(data.endcode())

    def run(self):
        data = self.get_data_from_client()
        json_data = json.loads(data)
        if json_data["type"] == "log-in":
            success, massage = self.database.check_user(json_data["username"], json_data["password"])
            if not success:
                self.client_socket.send(json.dumps({"type": "failed", "massage": massage}))
            else:
                auth_code = self.database.get_auth_code(json_data["username"])
                self.client_socket.send(json.dumps({"type": "success", "auth_code": auth_code}))


def main():
    pass


if __name__ == '__main__':
    main()
