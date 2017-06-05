import threading

from server.server import SocketServer
from Common.model import *

class GameState:
    waiting,\
    starting,\
    question_in_progress,\
    waiting_after_question,\
    stopping,\
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
    TIME_TO_START = 15
    MIN_PLAYERS = 2
    WAITING_TIME = 5
    AMOUNT_OF_QUESTIONS = 7

    def __init__(self, address, state_update_callback):
        self.clients = {}
        self.socket = KahootServerSocket(address, handler=self)
        self.state_update_callback = state_update_callback

        # Game variables
        self.current_question = Question
        self.quiz = None
        self.current_state = GameState.waiting

    def start(self):
        self.socket.run()

    def get_online_users(self):
        return filter(lambda tup: tup[0] != None, filter(None, self.clients.values()))

    def get_online_users_count(self):
        return len(self.get_online_users())

    def set_quiz(self, quiz):
        if isinstance(quiz, Quiz):
            self.quiz = quiz
        else:
            raise ValueError('Quiz should only be of type: "Quiz"')

    def handle_message(self, client, data):
        data = json.loads(data)
        if data['type'] == 'auth':
            self.clients[client] = (data['data'], False)
            online_users_count = self.get_online_users_count()
            if online_users_count >= KahootServer.MIN_PLAYERS and (self.current_state == GameState.waiting):
                # Telling the game to start his 'KahootServer.TIME_TO_START' seconds timer before game starts
                self.update_state(GameState.starting, time=KahootServer.TIME_TO_START)
        elif data['type'] == 'answer':
            answer_id = data['data']
            correct = answer_id == self.current_question.correct_answer.id
            self.clients[client] = (self.clients[client][0], correct)

    def send_question(self):
        online_users_count = self.get_online_users_count()
        if online_users_count < KahootServer.MIN_PLAYERS:
            self.update_state(GameState.stopping, message="Not enough players to start the game...")
            return
        next_question = self.quiz.get_next_question()
        if next_question: # If there is a question
            # Setting the current question for checking correct answers
            self.current_question = next_question
            self.update_state(GameState.question_in_progress, question=next_question)
        else: # If not, the game has ended
            self.update_state(GameState.ended)

    def broadcast(self, data):
        for (socket, (username, current_answer)) in self.clients.iteritems():
            if username != None:
                socket.send(data)

    def update_state(self, new_state, **kwargs):
        self.current_state = new_state
        # Updating controller
        self.state_update_callback(new_state, **kwargs)

    def wait_after_question(self):
        self.update_state(GameState.waiting_after_question, waiting_time=KahootServer.WAITING_TIME)

    def handle_disconnect(self, client):
        del self.clients[client]
        # Stop waiting if less than KahootServer.MIN_PLAYERS players are online
        online_users_count = self.get_online_users_count()
        if self.current_state == GameState.starting and online_users_count < KahootServer.MIN_PLAYERS:
            self.update_state(GameState.stopping, message="Not enough players to start the game...")

    def handle_connect(self, client):
        self.clients[client] = (None, False)


class Controller:
    def __init__(self):
        self.game_manager = KahootServer(('0.0.0.0', 8080), self.state_updated) # This is our model
        self.game_manager.set_quiz(Quiz.load_quiz(KahootServer.AMOUNT_OF_QUESTIONS)) # Loading quiz
        self.wait_for_clients()

    # This function updates all the connected players what other players are waiting for updating the waiting screen.
    # The loop stops automatically when the game is not in waiting state, this is why it should be called manually.
    def wait_for_clients(self):
        self.game_manager.current_state = GameState.waiting
        thread = threading.Thread(target=self.update_clients_waiting_screen)
        thread.daemon = True
        thread.start()

    def update_clients_waiting_screen(self):
        import time
        while 1:
            if not (self.game_manager.current_state==GameState.waiting or
                            self.game_manager.current_state==GameState.starting):
                break
            # Do the updating here
            self.game_manager.broadcast(json.dumps({'type': 'waiting', 'data': self.game_manager.get_online_users()}))
            time.sleep(0.5)

    def start_server(self):
        self.game_manager.start()

    def start_game(self):
        self.game_manager.send_question()

    def state_updated(self, state, **kwargs):
        if state == GameState.starting:
            print "Game starting in " + str(kwargs['time']) + " seconds."
            self.game_manager.broadcast(json.dumps({'type':'starting', 'data':{'time': kwargs['time']}}))
            self.timer(kwargs['time'], update_callback=None, finished_callback=self.start_game)
        elif state == GameState.stopping:
            print "Stopping game, " + str(kwargs['message'])
            self.game_manager.broadcast(json.dumps({'type':'stopping', 'data':{'message': kwargs['message']}}))
            # Waiting for clients again, doing this after 1.5 seconds so the previous waiting for clients block can be closed
            self.timer(1.5, finished_callback=self.wait_for_clients, update_callback=None)
        elif state == GameState.question_in_progress:
            print "Sending question."
            # Sending question to everybody
            self.game_manager.broadcast(json.dumps({'type': 'question', 'data': kwargs['question'].dict()}))
            question = kwargs['question']
            if not isinstance(question, Question):
                raise ValueError("A question passed must be of type 'Question'")
            # Setting question
            self.timer(question.time, update_callback=None, finished_callback=self.wait_after_question)
        elif state == GameState.waiting_after_question:
            for client in self.game_manager.clients.keys():
                username = self.game_manager.clients[client][0]
                if username == None:
                    continue
                correct = self.game_manager.clientss[client][1]
                print "User %s was %s." % (username, "correct" if correct else "wrong")
                client.send(json.dumps({'type': 'waiting_after_question', 'data': {'correct': correct,
                                                                                   'message': 'You were correct.' if correct else 'You were wrong.'}}))
                # Resetting answer
                self.game_manager.clients[client] = (username, False)
            print "Waiting after question for " + str(kwargs['waiting_time']) + " seconds."
            self.timer(kwargs['waiting_time'], update_callback=None, finished_callback=self.game_manager.send_question)
        elif state == GameState.ended:
            self.game_manager.set_quiz(Quiz.load_quiz(KahootServer.AMOUNT_OF_QUESTIONS))

    def wait_after_question(self):
        self.game_manager.wait_after_question()

    def timer(self, time, update_callback, finished_callback):
        print str(time)+'...',
        if update_callback:
            update_callback(time)
        if time <= 0:
            print ''
            finished_callback()
            return
        t = threading.Timer(1, lambda: self.timer(time-1, update_callback, finished_callback))
        t.start()

def main():
    kahoot_server = Controller()
    kahoot_server.start_server()

if __name__ == "__main__":
    main()
