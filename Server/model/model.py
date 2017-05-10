import uuid


class Question(dict):
    """
    A class that inherits from dictionary and is reassembling a trivia question,
    The first answer in the answers array is the correct answer
    """
    def __init__(self, question, answers, time):
        dict.__init__(self, question=question, answers=map(Answer, answers), time=time, id=str(uuid.uuid4()))


class Answer(dict):
    def __init__(self, answer):
        dict.__init__(self, answer=answer, id=str(uuid.uuid4()))


class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self._questions = self.questions[-1::]

    def get_next_question(self):
        if len(self._questions) == 0:
            return None
        return self._questions.pop()

    def load_quiz(self, amount_of_questions):
        # TODO: Load a quiz from the Trivia Questions Folder
        pass
