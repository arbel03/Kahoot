import socket
import threading


class SocketServer(socket.socket):
    _clients = []

    def __init__(self, address):
        socket.socket.__init__(self)
        # To silence- address occupied!!
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(address)
        self.listen(20)

    def run(self):
        print "Server started"
        try:
            self.accept_clients()
        except Exception as ex:
            print ex
        finally:
            print "Server closed"
            for client in self._clients:
                client.close()
            self.close()

    def accept_clients(self):
        while 1:
            (clientsocket, address) = self.accept()
            # Adding client to clients list
            self._clients.append(clientsocket)
            # Client Connected
            self.onopen(clientsocket)
            # Receiving data from client
            thread = threading.Thread(target=self.receive, args=(clientsocket,))
            thread.daemon = True
            thread.start()

    def receive(self, client):
        while 1:
            try:
                data = client.recv(1024)
            except:
                break
            if data == '':
                break
            # Message Received
            self.onmessage(client, data)
        # Removing client from clients list
        self._clients.remove(client)
        # Client Disconnected
        self.onclose(client)
        # Closing connection with client
        client.close()
        return

    def broadcast(self, message):
        # Sending message to all clients
        for client in self._clients:
            client.send(message)

    def close_client(self, client):
        if client in self._clients:
            self._clients.remove(client)
            client.close()

    def onopen(self, client):
        pass

    def onmessage(self, client, message):
        pass

    def onclose(self, client):
        pass