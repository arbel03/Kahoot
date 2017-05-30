import uuid
import json


class Question(object):
    """
    A class that inherits from dictionary and is reassembling a trivia question,
    The first answer in the answers array is the correct answer
    """
    def __init__(self, question, correct_answer, wrong_answers, time):
        self.time = time
        self.question = question
        self.correct_answer = correct_answer
        self.answers = wrong_answers
        self.answers.append(correct_answer)

    def get_answers(self):
        import random
        ans = self.answers[:]
        random.shuffle(ans)
        print ans
        return ans

    def get_correct_answer(self):
        return self.correct_answer

    @staticmethod
    def get_question_time(difficulty):
        difficulties = {'easy': 15, 'medium': 20, 'hard': 30}
        return difficulties[difficulty] if difficulty in difficulties.keys() else 45


class Answer(object):
    def __init__(self, answer):
        self.answer = answer
        self.id = str(uuid.uuid4())

    def __repr__(self):
        # So __dict__ of question will include the __dict__ of answer
        return str(self.__dict__)


class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self._questions = self.questions[::-1]
        print self._questions

    def get_next_question(self):
        if len(self._questions) == 0:
            return None
        return self._questions.pop()

    @staticmethod
    def load_quiz(amount_of_questions):
        import random
        # TODO: Load a quiz from the Trivia Questions Folder
        trivia_questions = open('Trivia Questions/Trivia Questions.txt', 'r')
        _questions = json.loads(trivia_questions.read())
        if amount_of_questions > len(_questions):
            raise ValueError("Max amount of questions is " + str(len(_questions)))
        questions = []
        while len(questions) < amount_of_questions:
            trivia_question = random.choice(_questions)
            while trivia_question in questions:
                trivia_question = random.choice(_questions)

            print 'Correct answer: ' + trivia_question['correct_answer']
            q = Question(question=trivia_question['question'],
                         correct_answer=Answer(trivia_question['correct_answer']),
                         wrong_answers=map(Answer, trivia_question['incorrect_answers']),
                         time=Question.get_question_time(trivia_question['difficulty']))
            questions.append(q)
        return Quiz(questions)
