import socket

from client_handler import ClientHandler


class Server:
    def __init__(self):
        self.server_socket = socket.socket()
        self.connected_client_list = {}

    def initialize_socket(self):
        self.server_socket.bind(('0.0.0.0', 1902))
        self.server_socket.listen(1)

    def connect_clients(self):
        """
        accept new client socket from the server socket and return the client socket object
        :return obj:
        """
        client_socket, client_address = self.server_socket.accept()
        print("new client connected", client_address)
        return client_socket


def main():
    server = Server()
    server.initialize_socket()
    while True:
        client_socket = server.connect_clients()
        c = ClientHandler(client_socket, server.connected_client_list)
        c.start()


if __name__ == '__main__':
    main()
