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
        self.wrong_answers = wrong_answers

    def get_answers(self):
        import random
        ans = self.wrong_answers
        ans.append(self.correct_answer)
        random.shuffle(ans)
        return ans

    def get_correct_answer(self):
        return self.correct_answer

    def dict(self):
        return {'time': self.time,
                'question': self.question,
                'correct_answer': self.correct_answer.__dict__,
                'wrong_answers': map(lambda ans: ans.__dict__, self.wrong_answers)}

    @staticmethod
    def get_question_time(difficulty):
        difficulties = {'easy': 15, 'medium': 20, 'hard': 30}
        return difficulties[difficulty] if difficulty in difficulties.keys() else 45

    @staticmethod
    def parse_question(obj):
        return Question(question=obj['question'],
                        correct_answer=Answer.parse_answer(obj['correct_answer']),
                        wrong_answers=map(Answer.parse_answer, obj['wrong_answers']),
                        time=obj['time'])


class Answer(object):
    def __init__(self, answer, id=None):
        self.answer = str(answer)
        if id:
            self.id = id
        else:
            self.id = str(uuid.uuid4())

    @staticmethod
    def parse_answer(obj):
        return Answer(obj['answer'], obj['id'])

    def __repr__(self):
        # So __dict__ of question will include the __dict__ of answer
        return self.__dict__

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self._questions = self.questions[::-1]

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

            #print 'Correct answer: ' + trivia_question['correct_answer']
            q = Question(question=trivia_question['question'],
                         correct_answer=Answer(trivia_question['correct_answer']),
                         wrong_answers=map(Answer, trivia_question['incorrect_answers']),
                         time=Question.get_question_time(trivia_question['difficulty']))
            questions.append(q)
        return Quiz(questions)

class Score(object):
    pass