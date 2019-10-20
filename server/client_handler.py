import threading


class ClientHandler(threading.Thread):
    def __init__(self, client_socket, server):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.server = server

    def get_data_from_client(self):
        return self.client_socket.recv(1024).decode()

    def send_data_to_client(self, data):
        self.client_socket.send(data.endcode())

    def run(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
