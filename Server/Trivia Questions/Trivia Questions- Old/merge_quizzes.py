import os
import glob
import json

_questions = []
for file in os.listdir(os.curdir):
    if file.endswith('.txt'):
        json_file = open(file, 'r')
        questions = json.loads(json_file.read())
        print questions
        _questions += questions
        print "Opening", file
        json_file.close()

merged_file = open('Trivia Questions.txt', 'w')
merged_file.write(json.dumps(_questions))
merged_file.close()

print len(_questions)
