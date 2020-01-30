from app import db
from app.models import Song, Answer

count = 1
to_fix = {}

while count <= 125:
    answer = Answer.query.get(count)
    options = answer.answers.split(',')
    ans_list = []
    for ans in options:
        if '-' not in ans:
            ans_list.append(ans)
    to_fix[count] = ans_list
    count = count + 1

outF = open('ans to fix(checked).txt', 'w')
for key, value in to_fix.items():
    outF.write(str(key))
    outF.write(': ')
    value = ', '.join(value)
    outF.write(value)
    outF.write('\n')
outF.close()
