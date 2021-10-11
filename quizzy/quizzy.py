from flask import (Flask, render_template, request, escape,
                    url_for, redirect, make_response, session)
import random
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = b'Lr\x9b\x81o\xa9U\x9f>\x9e\xae7qD\xfbZ'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
##################GETQUESTION

def save_session():
    db_conn = sqlite3.connect('quizzy.db');
    cursor = db_conn.cursor();
    _sql = """INSERT INTO user
    (username, create_date, category,correct_answers, browser)
    values (?,?,?,?,?)"""
    cursor.execute(_sql, (session['username'],
                        datetime.utcnow(),
                        session['category'],
                        session['score'],
                        request.user_agent.browser,
                        ));
    db_conn.commit();
    print("LOG SAVED")
    cursor.close();        # Close the database connection
    db_conn.close();


def get_question(category):
    db_conn = sqlite3.connect('quizzy.db');
    cursor = db_conn.cursor();
    _sql = """SELECT Q.question_id, Q.question, Q.correct_choice, Q.choice1,
    Q.choice2, Q.choice3 FROM question Q
    LEFT JOIN category_question C
    ON Q.cat_id = C.cat_id
    WHERE C.category = ?
    ORDER BY RANDOM() ;"""
    cursor.execute(_sql, (category,));
    question_data = cursor.fetchall()
    cursor.close();        # Close the database connection
    db_conn.close();
    print(question_data)
    return question_data

@app.route('/')
@app.route('/entry', methods=['Get','POST'])
def index():
    return render_template('entry.html',
                            the_title = 'Welcome to Quizzy!',
                            )

@app.route('/category', methods = ['Get','POST'])
def choose_category():
    session['username'] = request.form['nickname']
    session['score'] = 0
    session['time']  = 0
    return render_template('category.html',
                            the_title = 'please choose the category: ',
                            nickname = session['username'])

@app.route('/category', methods = ['Get','POST'])
def get_questions():
    for k,v in request.form.items():
        print(k,"!!!!!!!!!!!!!!!!!!!!!",v,"!!!!!!!!!!!!!!!!!!!!!")
    session['category'] = k
    category = session['category']
    questions = get_question(category)
    return questions

@app.route('/quiz', methods =['GET','POST'])
def quiz():
            if  session['time'] == 0:
                session['questions'] = get_questions()
            elif session['time'] == len(session['questions']):
                save_session()
                return render_template('review.html')
            else:
                pass
            data = session['questions']
            question = data[session['time']][1]
            question_id = data[session['time']][0]
            real_answer = data[session['time']][2]
            print(question)
            choices = data[session['time']][2:6]
            choice = []
            for i in choices:
                choice.append(i)
            random.shuffle(choice)
            session['real_answer'] = real_answer
            session['time'] += 1
            print("real_answer is:", real_answer)
            return render_template('quiz.html',
        the_question = question,
        the_title = 'Quiz',
        a = choice[0],
        b = choice[1],
        c = choice[2],
        d = choice[3])

@app.route('/quiz', methods =['GET','POST'])
def get_score():
    if request.method == 'POST':
        for k,v in request.form.items():
            print(k,"!!!!!!!!!!!!!!!!!!!!!",v,"!!!!!!!!!!!!!!!!!!!!!")
            user_answer = v
        if user_answer[3:] == session['real_answer']:
            session['score'] += 1
            session['is_correct'] = "Congrats!"
        else:
            session['is_correct'] = "Wrong"


@app.route('/answer', methods =['GET','POST'])
def check_answer():
    get_score()
    total = session['time']
    return render_template('answer.html',total =  total)


app.run(debug = True, port = 8000, host = '0.0.0.0')
