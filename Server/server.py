import json
import threading
from Tkinter import Tk
import time

from Common.GameScreen import GameScreen
from Server.view.WaitingScreen import WaitingScreen
from server.server import SocketServer
from Common.model.model import *

class GameState:
    waiting,\
    starting,\
    question_in_progress,\
    waiting_after_question,\
    stopping, \
    ended = range(6)

class KahootServerSocket(SocketServer):
    def __init__(self, address, handler):
        SocketServer.__init__(self, address)
        self.handler = handler

    def onopen(self, client):
        self.handler.handle_connect(client)

    def onmessage(self, client, message):
        self.handler.handle_message(client, message)

    def onclose(self, client):
        self.handler.handle_disconnect(client)


class KahootServer():
    TIME_TO_START = 10
    MIN_PLAYERS = 1
    WAITING_TIME = 10

    def __init__(self, address, state_update_callback):
        self.clients = {}
        self.socket = KahootServerSocket(address, handler=self)
        self.state_update_callback = state_update_callback

        # Game variables
        self.in_game = False
        self.quiz = None
        self.current_state = GameState.waiting

    def start(self):
        thread = threading.Thread(target=self.socket.run)
        thread.daemon = True
        thread.start()

    def get_online_users_count(self):
        return len(filter(lambda tup: tup[0] != None, self.clients.values()))

    def set_quiz(self, quiz):
        if isinstance(quiz, Quiz):
            self.quiz = quiz
        else:
            raise ValueError('Quiz should only be of type: "Quiz"')

    def handle_message(self, client, data):
        data = json.loads(data)
        if data['type'] == 'auth':
            self.clients[client] = (data['data'], None)
            online_users_count = self.get_online_users_count()
            if online_users_count >= KahootServer.MIN_PLAYERS and self.current_state == GameState.waiting:
                # Telling the game to start his 30 seconds timer before game starts
                self.update_state(GameState.starting, time=KahootServer.TIME_TO_START)

    def send_question(self):
        print "Sending question!"
        online_users_count = self.get_online_users_count()
        if online_users_count < KahootServer.MIN_PLAYERS:
            self.update_state(GameState.stopping)
            return
        next_question = self.quiz.get_next_question()
        print next_question
        if next_question: # If there is a question
            self.update_state(GameState.question_in_progress, question=next_question)
        else: # If not, the game has ended
            self.update_state(GameState.ended)

    def update_state(self, new_state, **kwargs):
        self.current_state = new_state
        # Updating controller
        self.state_update_callback(new_state, **kwargs)

    def wait_after_question(self):
        # TODO: Send the clients their status, correct/not, and position
        # Can pass here top scores and display on the wall
        self.update_state(GameState.waiting_after_question, waiting_time=KahootServer.WAITING_TIME)

    def handle_disconnect(self, client):
        del self.clients[client]
        # Stop waiting if less than KahootServer.MIN_PLAYERS players are online
        online_users_count = self.get_online_users_count()
        if self.current_state == GameState.starting and online_users_count < KahootServer.MIN_PLAYERS:
            self.update_state(GameState.stopping)

    def handle_connect(self, client):
        self.clients[client] = None


class Controller:
    def __init__(self, root):
        self.root = root

        # Setting fullscreen is the best
        self.root.attributes('-fullscreen', True)
        # To silently close threads and after too...
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        # Adding screens
        self.game_screen = GameScreen(self.root)
        self.add_screen(self.game_screen)
        self.waiting_screen = WaitingScreen(self.root)
        self.add_screen(self.waiting_screen)

        self.game_manager = KahootServer(('0.0.0.0', 8080), self.state_updated) # This is our model
        self.game_manager.set_quiz(Quiz.load_quiz(7)) # Loading quiz

        self.wait_for_clients()

    def wait_for_clients(self):
        # Update clients view every 1 second
        self.show_screen(self.waiting_screen)
        # Work around cus cant dispatch main thread in python
        self.clients_updated()

    def add_screen(self, screen):
        screen.pack(side="top", fill="both", expand=True)
        screen.pack_forget()

    def show_screen(self, screen):
        # Removing all other screens
        for slave in self.root.pack_slaves():
            slave.pack_forget()
        screen.pack(side="top", fill="both", expand=True)

    def start_server(self):
        #Running kahoot server
        self.game_manager.start()

    def start_game(self):
        self.show_screen(self.game_screen)
        self.game_manager.send_question()

    def clients_updated(self):
        self.waiting_screen.update_usernames(map(lambda user: user[0], filter(lambda user: user is not None, self.game_manager.clients.values())))
        if self.game_manager.current_state == GameState.waiting or GameState.starting:
            self.root.after(1000, self.clients_updated)

    def state_updated(self, state, **kwargs):
        if state == GameState.starting:
            print "Game starting in " + str(kwargs['time']) + " seconds."
            self.timer(kwargs['time'], update_callback=self.waiting_screen.update_countdown, finished_callback=self.start_game)
        elif state == GameState.stopping:
            print "Stopping game cus one of the clients disconnected."
            wait_for_clients()
            self.waiting_screen.set_info_label('Not enough players, waiting for more...')
        elif state == GameState.question_in_progress:
            print "Displaying question"
            question = kwargs['question']
            if not isinstance(question, Question):
                raise ValueError("A question passed must be of type 'Question'")
            # Setting question
            self.game_screen.update_question(question)
            self.timer(question.time, update_callback=self.game_screen.update_countdown, finished_callback=self.wait_after_question)
        elif state == GameState.waiting_after_question:
            print "Waiting after question for " + str(kwargs['waiting_time']) + " seconds."
            self.timer(kwargs['waiting_time'], update_callback=None, finished_callback=self.game_manager.send_question)

    def wait_after_question(self):
        self.game_manager.wait_after_question()

    def timer(self, time, update_callback, finished_callback):
        if update_callback:
            update_callback(time)
        if time == 0:
            finished_callback()
            return
        self.root.after(1000, func=lambda: self.timer(time-1, update_callback, finished_callback))

def main():
    root = Tk()
    kahoot_server = Controller(root)
    kahoot_server.start_server()
    root.mainloop()


if __name__ == "__main__":
    main()
