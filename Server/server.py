from Tkinter import Tk
from view.GameScreen import GameScreen
from view.WaitingScreen import WaitingScreen
from SimpleWebSocketServer import *
from HTTPServer.RootedHTTPServer import *
import os
import threading
import json


class KahootServer(SimpleWebSocketServer):
    class KahootClient(WebSocket):
        """This is a class handler for websockets clients,
        Changing static members to functions are a way to communicate between an object
        and this class interface"""

        def handleMessage(self):
            # echo message back to client
            try:
                self.handler.handle_message(self, str(self.data))
            except ValueError as ex:
                print ex

        def handleConnected(self):
            self.handler.clients[self] = None
            print self.address, "connected"

        def handleClose(self):
            self.handler.client_disconnected(self)
            print self.address, "disconnected"

    def __init__(self, address):
        self.KahootClient.handler = self
        self.clients = {}
        SimpleWebSocketServer.__init__(self, address[0], address[1], self.KahootClient)

    def handle_message(self, client, data):
        data = json.loads(data)
        if data['type'] == 'auth':
            self.clients[client] = (data['data'], None)
            self.clients_updated()

    def client_disconnected(self, client):
        # If the client was in the game we update the usernames screen
        if client in self.clients.keys():
            self.clients_updated()
        del self.clients[client]

class Controller:
    def __init__(self, root):
        self.root = root

        self.game_screen = GameScreen(self.root)
        self.waiting_screen = WaitingScreen(self.root)
        #self.add_screen(self.game_screen)
        self.add_screen(self.waiting_screen)
        self.show_screen(self.waiting_screen)

        self.websocket_server = KahootServer(('', 8080))
        self.websocket_server.clients_updated = self.clients_updated
        # HTTP server in a specific path
        self.http_server = RootedHTTPServer(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'\Client',\
                                            ('', 80), \
                                            RootedHTTPRequestHandler)
        #self.root.attributes('-fullscreen', True)

    def add_screen(self, screen):
        screen.pack(side="top", fill="both", expand=True)
        screen.pack_forget()

    def show_screen(self, screen):
        screen.pack(side="top", fill="both", expand=True)

    def start_servers(self):
        http_server_thread = threading.Thread(target=self.http_server.serve_forever)
        websocket_server_thread = threading.Thread(target=self.websocket_server.serveforever)
        http_server_thread.start()
        websocket_server_thread.start()
        print "Servers started servers"

    def clients_updated(self):
        self.waiting_screen.update_usernames(map(lambda user: user[0], self.websocket_server.clients.values()))

def main():
    root = Tk()
    kahoot_server = Controller(root)
    kahoot_server.start_servers()
    root.mainloop()

if __name__ == "__main__":
    main()
