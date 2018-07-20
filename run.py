#-*-coding:utf-8-*-
from flask import Flask, g, flash, redirect, url_for,jsonify
from flask import render_template
from flask import request,session
from server import get_user_question,update_user_question

app=Flask(__name__)

@app.route('/question/<user_id>',methods=['GET','POST'])
def question(user_id):
    if request.method=='POST':
        try:
            update_user_question(**request.form)
        except Exception as e:
            return e
        return jsonify('seccess')

    question_id,data,undone = get_user_question(user_id)
    return jsonify({'questionId':question_id,
                    'title':data[0],
                    'options':[data[1],data[2],data[3],data[4]],
                    'attributes':{
                        'questionID':question_id,
                        'answer':data[6],
                        'answerExplain':data[5],
                        },
                    'totalQuestionNumber':undone,
                    })

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)
