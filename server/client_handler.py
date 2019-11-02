import json
import threading

import database


class ClientHandler(threading.Thread):
    def __init__(self, client_socket, connected_client_list):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.connected_client_list = connected_client_list

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
        elif json_data["type"] == "sign-in":
            account_database = database.AsycDatabase("database.db")
            success, massage = account_database.create_user(json_data["username"], json_data["password"])
            if not success:
                self.send_data_to_client(json.dumps({"type": "failed", "massage": massage}).encode())
            else:
                self.send_data_to_client(json.dumps({"type": "success", "massage": massage}).encode())
        elif json_data["type"] == "get-id-list":
            account_database = database.AsycDatabase("database.db")
            authenticated, user_id = account_database.authentication_user(json_data["auth_code"])
            if authenticated:
                id_list = account_database.get_id_list(user_id)
                self.send_data_to_client(json.dumps({"type": "success", "data": id_list}).encode())
            else:
                self.send_data_to_client(
                    json.dumps({"type": "failed", "error_massage": "unauthenticated user"}).encode())
        elif json_data["type"] == "get-username-from-id":
            account_database = database.AsycDatabase("database.db")
            authenticated = account_database.authentication_user(json_data["auth_code"])[0]
            if authenticated:
                username = account_database.get_username_from_id(json_data["user_id"])
                self.send_data_to_client(json.dumps({"type": "success", "data": username}).encode())
            else:
                self.send_data_to_client(
                    json.dumps({"type": "failed", "error_massage": "unauthenticated user"}).encode())
        elif json_data["type"] == "get-massages":
            account_database = database.AsycDatabase("database.db")
            authenticated, user_id = account_database.authentication_user(json_data["auth_code"])
            if authenticated:
                self.connected_client_list[user_id] = self.client_socket
        elif json_data["type"] == "send-massage":
            account_database = database.AsycDatabase("database.db")
            authenticated, user_id = account_database.authentication_user(json_data["auth_code"])
            if authenticated:
                if json_data["to"] == "all":
                    data = {"user_id": user_id, "massage": json_data["data"], "to": "all"}
                    for user in self.connected_client_list:
                        if user != user_id:
                            self.connected_client_list[user].send(json.dumps(data).encode())
                    data = {"type": "success"}
                    self.send_data_to_client(json.dumps(data).encode())
                else:
                    data = {"user_id": user_id, "massage": json_data["data"]}
                    self.connected_client_list[json_data["to"]].send(json.dumps(data).encode())
                    data = {"type": "success"}
                    self.send_data_to_client(json.dumps(data).encode())
            else:
                self.send_data_to_client(
                    json.dumps({"type": "failed", "error_massage": "unauthenticated user"}).encode())


def main():
    pass


if __name__ == '__main__':
    main()
