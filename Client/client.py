import Tkinter as tk
from Common.GameScreen import GameScreen
from view.InfoScreen import InfoScreen
import socket
import json


class Controller:
    def __init__(self, root, is_wall):
        self.root = root
        self.is_wall = is_wall
        self.set_geometry(500, 1000)

        self.game_screen = GameScreen(self.root)
        self.info_screen = InfoScreen(self.root)

        self.add_screen(self.info_screen)
        self.add_screen(self.game_screen)
        self.show_screen(self.info_screen)

        self.socket = socket.socket()

        self.connect()

    def connect(self):
        try:
            self.socket.connect(('127.0.0.1', 8080))
            self.info_screen.set_text('Connecting...')
            self.socket.send(json.dumps({'type':'auth', 'data': 'arbel03'}))
            self.info_screen.set_text('Connected')

        except socket.error as ex:
            print ex
            if ex.errno == 10061:
                self.info_screen.set_text('Server is not active')
            else:
                self.info_screen.set_text('Failed connecting to the server...')
            # Closing the screen
            self.root.after(3000, self.root.destroy)

    def set_geometry(self, height, width):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry('%dx%d+%d+%d'%(width, height, screen_width/2-width/2, screen_height/2-height/2))

    def add_screen(self, screen):
        screen.pack(side="top", fill="both", expand=True)
        screen.pack_forget()

    def show_screen(self, screen):
        screen.pack(side="top", fill="both", expand=True)


def main():
    root = tk.Tk()
    app = Controller(root, is_wall=raw_input("Is this client a wall?: "))
    root.mainloop()


if __name__ == '__main__':
    main()
