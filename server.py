import sqlite3
import re
import datetime
import random

def update_user_question(**data):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('insert into user_questions (user_id,question_id,result,\
                choice) values(?,?,?,?)',\
                    (data['userId'][0],data['questionId'][0],\
                    data['answerResult'][0],data['userChoice'][0]))
    conn.commit()
    conn.close()

def get_user_question(user_id):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select question_id from user_questions where user_id=?',(user_id,))
    done=[x[0] for x in cursor.fetchall()]
    cursor.execute('select id from questions')
    questions= [x[0] for x in cursor.fetchall()]
    conn.close()
    undone=[]
    for q in questions:
        if q not in done:
            undone.append(q)
    r=random.choice(undone)
    return [r,get_question(r),len(undone)-1]


def get_question(question_id):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select title,A,B,C,D,explain,answer from questions where id=?',(question_id,))
    data,=cursor.fetchall()
    conn.close()
    return data
