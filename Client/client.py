try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import socket
import threading
import Queue

from Common.model import *
from Client.view.GameScreen import GameScreen
from Client.view.WaitingScreen import WaitingScreen
from Client.view.WaitingAfterQuestionScreen import WaitingAfterQuestionScreen


class Controller:
    def __init__(self, root):
        self.root = root
        self.set_geometry(500, 1000)

        # UI
        self.game_screen = GameScreen(self.root)
        self.waiting_screen = WaitingScreen(self.root)
        self.waiting_after_question_screen = WaitingAfterQuestionScreen(self.root)

        # Configuring UI
        self.game_screen.buttons.set_button_callback(self.button_clicked)

        self.add_screen(self.waiting_after_question_screen)
        self.add_screen(self.waiting_screen)
        self.add_screen(self.game_screen)
        self.show_screen(self.waiting_screen)

        # Current question for sending answers back to the server
        self.current_answers = None

        # Queue + socket
        self.queue = Queue.Queue()
        self.socket = socket.socket()
        self.update()

        self._job = None

    def update(self):
        try:
            while 1:
                response = self.queue.get_nowait()
                self.handle_response(response)
                self.root.update_idletasks()
        except Queue.Empty:
            pass
        self.root.after(100, self.update)

    def button_clicked(self, button):
        self.game_screen.buttons.disable()
        self.socket.send(json.dumps({'type': 'answer', 'data': self.current_answers[button].id}))

    def handle_response(self, response):
        temp = json.loads(response)
        if temp['type'] == 'waiting':
            self.waiting_screen.update_usernames(map(lambda tup: tup[0], temp['data']))
        elif temp['type'] == 'starting':
            self.timer(temp['data']['time'],
                       update_callback=self.waiting_screen.update_countdown,
                       finished_callback=lambda: self.show_screen(self.game_screen))
        elif temp['type'] == 'stopping':
            if self._job:
                self.root.after_cancel(self._job)
            self.show_screen(self.waiting_screen)
            self.waiting_screen.set_info_label(temp['data']['message'])
            self.waiting_screen.update_usernames([])
        elif temp['type'] == 'question':
            question = Question.parse_question(temp['data'])
            self.show_screen(self.game_screen)
            # Updating the screen with the question and getting an array with the current answers, shuffled
            self.current_answers = self.game_screen.update_question(question)
            # Setting buttons enabled
            self.game_screen.buttons.enable()
            self.timer(question.time, update_callback=self.game_screen.update_countdown, finished_callback=None)
        elif temp['type'] == 'waiting_after_question':
            self.waiting_after_question_screen.set_correct(temp['data']['correct'], temp['data']['message'])
            self.show_screen(self.waiting_after_question_screen)

    def connect(self):
        try:
            self.socket.connect(('127.0.0.1', 8080))
            self.waiting_screen.set_info_label('Connecting...')
            self.socket.send(json.dumps({'type': 'auth', 'data': raw_input("Enter your username: ")}))
            self.waiting_screen.set_info_label('Connected')

            listenning_thread = threading.Thread(target=self.receive)
            listenning_thread.daemon = True
            listenning_thread.start()

            return True
        except socket.error as ex:
            print ex
            if ex.errno == 10061:
                self.waiting_screen.set_info_label('Server is not active')
            else:
                self.waiting_screen.set_info_label('Failed connecting to the server...')
            # Closing the screen
            self.root.after(3000, self.root.destroy)
        return False

    def receive(self):
        print "Running"
        while True:
            try:
                data = self.socket.recv(1024)
            except:
                self.queue.put(json.dumps({'type': 'stopping', 'data': {'message': 'Disconnected from the server.'}}))
                break
            if data != '':
                self.queue.put(data)

    def set_geometry(self, height, width):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry('%dx%d+%d+%d'%(width, height, screen_width/2-width/2, screen_height/2-height/2))

    def add_screen(self, screen):
        screen.pack(side="top", fill="both", expand=True)
        screen.pack_forget()

    def show_screen(self, screen):
        # Removing all other screens
        for slave in self.root.pack_slaves():
            slave.pack_forget()
        screen.pack(side="top", fill="both", expand=True)

    def timer(self, time, update_callback, finished_callback):
        if update_callback:
            update_callback(time)
        if time == 0:
            if finished_callback:
                finished_callback()
            return
        self._job = self.root.after(1000, func=lambda: self.timer(time-1, update_callback, finished_callback))


def main():
    root = tk.Tk()
    app = Controller(root)
    app.connect()
    root.mainloop()

if __name__ == '__main__':
    main()
