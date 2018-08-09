#-*-coding:utf-8-*-
from flask import Flask, g, flash, redirect, url_for,jsonify,json
from flask import render_template
from flask import request,session
from server import get_user_question,update_user_question,get_done
from server import update_question,get_question_count,delete_history

app=Flask(__name__)

@app.route('/question/type=<q_type>/<user_id>',methods=['GET','POST'])
def question(user_id,q_type):
    if request.method=='POST':
        data=json.loads(request.get_data())
        try:
            update_user_question(**data)
        except Exception as e:
            return jsonify({'status':0,'Exception':str(e)})
        return jsonify({'status':1})

    try:
        question_id,data,undone = get_user_question(user_id,q_type)
    except Exception as e:
        return jsonify({'status':0,'Exception':str(e)})
    return jsonify({'status':1,
                    'data':{
                        'questionId':question_id,
                        'title':data[0],
                        'options':[data[1],data[2],data[3],data[4]],
                        'attributes':{
                            'questionID':question_id,
                            'answer':data[6],
                            'answerExplain':data[5],
                            },
                        'totalQuestionNumber':undone,
                        },
                    })

@app.route('/countquestion')
def countquestion():
    try:
        data=get_question_count()
    except Exception as e:
        return jsonify({'status':0,'Exception':str(e)})
    return jsonify({'status':1,'data':data})

@app.route('/historyquestion/<user_id>')
def historyquestion(user_id):
    try:
        data=get_done(user_id)
    except Exception as e:
        return jsonify({'status':0,'Exception':str(e)})
    return jsonify({'status':1,
                    'data':data,
                    })

@app.route('/updatequestion/',methods=['POST'])
def updatequestion():
    data=json.loads(request.get_data())
    try:
        update_question(data)
    except Exception as e:
        return jsonify({'status':0,'Exception':str(e)})
    return jsonify({'status':1})

@app.route('/delete_history',methods=['POST'])
def d_history():
    data=json.loads(request.get_data())
    try:
        delete_history(data)
    except Exception as e:
        return jsonify({'status':0,'Exception':str(e)})
    return jsonify({'status':1})

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)
