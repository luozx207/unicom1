import sqlite3
import re
from datetime import date
import random
import urllib3,json

def update_user_question(**data):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('insert into user_questions (user_id,question_id,result,\
                choice) values(?,?,?,?)',\
                    (data['userId'],data['questionId'],\
                    data['answerResult'],data['userChoice']))
    conn.commit()
    conn.close()

def get_user_question(user_id,q_type):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select question_id from user_questions where user_id=?',(user_id,))
    done=set([x[0] for x in cursor.fetchall()])
    if q_type=='0':
        cursor.execute('select id from questions')
    else:
        cursor.execute('select id from questions where q_type=?',(q_type,))
    questions= set([x[0] for x in cursor.fetchall()])
    conn.close()
    undone=list(questions-done)
    if len(undone)==0:
        return [0,0,0]
    r=random.choice(undone)
    return [r,get_question(r),len(undone)]


def get_question(question_id):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select title,A,B,C,D,explain,answer,q_type from questions where id=?',(question_id,))
    data,=cursor.fetchall()
    conn.close()
    return data

def get_question_count():
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select q_type from questions')
    data=cursor.fetchall()
    total=len(data)
    type_1=0
    type_2=0
    type_3=0
    type_4=0
    for d in data:
        if d[0]=="1":
            type_1+=1
        elif d[0]=="2":
            type_2+=1
        elif d[0]=="3":
            type_3+=1
        else:
            type_4+=1
    return {'total':total,'type_1':type_1,'type_2':type_2,
            'type_3':type_3,'type_4':type_4}

def get_done(user_id):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select question_id,choice from user_questions where user_id=? and result=0',(user_id,))
    done=cursor.fetchall()
    total=len(done)
    question_data=[]
    for d in done:
        data = get_question(d[0])
        question_data.append({'questionId':d[0],
                        'q_type':data[7],
                        'title':data[0],
                        'options':[data[1],data[2],data[3],data[4]],
                        'attributes':{
                            'answer':data[6],
                            'answerExplain':data[5],
                            },
                        'choice':d[1],
                        })
    return {'total':total, 'question_data':question_data}

def update_question(data):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('insert into questions (title,answer,A,B,C,D,\
                explain,q_type) values(?,?,?,?,?,?,?,?)',\
                    (data['title'],data['answer'],\
                    data['A'],data['B'],data['C'],\
                    data['D'],data['explain'],data['q_type']))
    conn.commit()
    conn.close()

def delete_history(data):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('update user_questions set result=1 where user_id=? and question_id=?',\
                    (data['user_id'],data['question_id']))
    conn.commit()
    conn.close()

def get_sign_info(user_id):
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select date from sign where user_id=?',(user_id,))
    all_date=set([x[0] for x in cursor.fetchall()])
    now_date=date.today().strftime('%Y-%m-%d')
    if now_date in all_date:
        signed=True
    else:
        signed=False
    total=len(all_date)
    conn.close()
    return {'total':total,'signed':signed}

def update_sign(user_id):
    now_date=date.today().strftime('%Y-%m-%d')
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute('select date from sign where user_id=?',(user_id,))
    all_date=set([x[0] for x in cursor.fetchall()])
    if now_date in all_date:
        raise Exception("今日已签到")
    else:
        #获取token
        http=urllib3.PoolManager()
        r=http.request('GET','https://www.tiucloud.cn/signed')
        d = json.loads(r.data.decode())
        #发送token，增加D币
        data={'token':d['token'],'userId':int(user_id)}
        encoded_data = json.dumps(data).encode('utf-8')
        http.request('POST','https://www.tiucloud.cn/signedadd',
                body=encoded_data,
                headers={'Content-Type':'application/json'})
        #增加签到信息
        cursor.execute('insert into sign (user_id,date) values(?,?)',\
                (user_id,now_date))
    conn.commit()
    conn.close()
