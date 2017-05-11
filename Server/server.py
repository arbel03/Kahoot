from Tkinter import Tk
from view.GameScreen import GameScreen
from view.WaitingScreen import WaitingScreen
from SimpleWebSocketServer import *
from HTTPServer.RootedHTTPServer import *
import os
import threading
import json


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
        del self.handler.clients[self]
        print self.address, "disconnected"


class KahootServer():
    def __init__(self, address):
        KahootClient.handler = self
        self.clients = {}
        self.websocket_server = SimpleWebSocketServer(address[0], address[1], KahootClient)

    def run(self):
        thread = threading.Thread(target=self.websocket_server.serveforever)
        thread.daemon = True
        thread.start()

    def handle_message(self, client, data):
        data = json.loads(data)
        if data['type'] == 'auth':
            print "Updating name to", data['data']
            self.clients[client] = (data['data'], None)

class Controller:
    def __init__(self, root):
        self.root = root

        self.game_screen = GameScreen(self.root)
        self.waiting_screen = WaitingScreen(self.root)
        #self.add_screen(self.game_screen)
        self.add_screen(self.waiting_screen)
        self.show_screen(self.waiting_screen)

        self.websocket_server = KahootServer(('0.0.0.0', 8080))
        self.websocket_server.clients_updated = self.clients_updated
        # HTTP server in a specific path
        self.http_server = RootedHTTPServer(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'\Client',\
                                            ('0.0.0.0', 8000), \
                                            RootedHTTPRequestHandler)
        #Update clients view every 1 second
        self.root.after(1000, self.clients_updated)
        self.root.attributes('-fullscreen', True)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def add_screen(self, screen):
        screen.pack(side="top", fill="both", expand=True)
        screen.pack_forget()

    def show_screen(self, screen):
        screen.pack(side="top", fill="both", expand=True)

    def start_servers(self):
        http_server_thread = threading.Thread(target=self.http_server.serve_forever)
        http_server_thread.daemon = True
        http_server_thread.start()
        #Running kahoot websocket server
        self.websocket_server.run()
        print "Servers started servers"

    def clients_updated(self):
        print self.websocket_server.clients.values()
        self.waiting_screen.update_usernames(map(lambda user: user[0], filter(lambda user: user is not None, self.websocket_server.clients.values())))
        self.root.after(1000, self.clients_updated)

def main():
    root = Tk()
    kahoot_server = Controller(root)
    kahoot_server.start_servers()
    root.mainloop()

if __name__ == "__main__":
    main()
