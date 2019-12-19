from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

import sqlite3

db = sqlite3.connect('test.db')
cur = db.cursor()

cur.execute("DROP TABLE IF EXISTS answers")
cur.execute("""CREATE TABLE answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    q1 TEXT,
    q2 TEXT,
    q3 TEXT,
    q4 TEXT,
    q5 TEXT,
    q6 INTEGER,
    q7 INTEGER,
    comment TEXT)
    """)

cur.execute("DROP TABLE IF EXISTS questions")
cur.execute("""CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT
    )""")

cur.execute("DROP TABLE IF EXISTS user")
cur.execute("""CREATE TABLE 
    user ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gender TEXT,
    education TEXT,
    age INTEGER,
    city TEXT,
    rus_level TEXT)""")

cur.execute("""INSERT INTO questions VALUES
    (1, 'Какого рода слово "худи"?'),
    (2, 'Какого рода слово "кофе"?'),
    (3, 'Какого рода слово "река"?'),
    (4, 'Какого рода слово "тапки"?'),
    (5, 'Какого рода слово "кроссовки"?'),
    (6, 'Даже Вася-то решил задачу?'),
    (7, 'Хорошо, что акцент у него хоть едва заметен.'
    )""")

db.commit()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Text)
    education = db.Column(db.Text)
    age = db.Column(db.Integer)
    city = db.Column(db.Text)
    rus_level = db.Column(db.Text)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)


class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    q1 = db.Column(db.Text)
    q2 = db.Column(db.Text)
    q3 = db.Column(db.Text)
    q4 = db.Column(db.Text)
    q5 = db.Column(db.Text)
    q6 = db.Column(db.Integer)
    q7 = db.Column(db.Integer)
    comment = db.Column(db.Text)

@app.route('/')
def instruction():
    return render_template('index.html')

@app.route('/questions')
def question_page():
    questions = Questions.query.all()
    return render_template(
        'questions.html',
        questions=questions
    )

@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('question_page'))
    gender = request.args.get('gender')
    education = request.args.get('education')
    age = request.args.get('age')
    city = request.args.get('city')
    rus_level = request.args.get('rus_level')
    user = User(
        age=age,
        gender=gender,
        education=education,
        city = city,
        rus_level = rus_level
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    q3 = request.args.get('q3')
    q4 = request.args.get('q4')
    q5 = request.args.get('q5')
    q6 = request.args.get('q6')
    q7 = request.args.get('q7')
    comment = request.args.get('comment')
    answer = Answers(id=user.id, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, comment=comment)
    db.session.add(answer)
    db.session.commit()
    return """<head><style>body {background-image: url(static/pod.png)}</style></head>
              <body>
              <p>Спасибо!</p>
              <p><a href='/stats'>Посмотреть статистику</a></p>
              </body>"""

@app.route('/stats')
def stats():
    all_info = {}
    age_stats = db.session.query(
        func.avg(User.age),
        func.min(User.age),
        func.max(User.age)
    ).one()
    all_info['age_mean'] = age_stats[0]
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    all_info['total_count'] = User.query.count()
    all_info['q6_mean'] = db.session.query(func.avg(Answers.q6)).one()[0]
    q6_answers = db.session.query(Answers.q6).all()
    all_info['q7_mean'] = db.session.query(func.avg(Answers.q7)).one()[0]
    q7_answers = db.session.query(Answers.q7).all()

    colours = ['blue', 'green', 'yellow', 'red', 'olive']

    all_info['q1_mean'] = db.session.query(Answers.q1).all()
    q1_answers = db.session.query((Answers.q1), func.count(Answers.id)).group_by(Answers.q1).all()
    labels1 = [q1_answers[i][0] for i in range(len(q1_answers))]
    values1 = [q1_answers[i][1] for i in range(len(q1_answers))]

    all_info['q2_mean'] = db.session.query(Answers.q2).all()
    q2_answers = db.session.query((Answers.q2), func.count(Answers.id)).group_by(Answers.q2).all()
    labels2 = [q2_answers[i][0] for i in range(len(q2_answers))]
    values2 = [q2_answers[i][1] for i in range(len(q2_answers))]

    all_info['q3_mean'] = db.session.query(Answers.q3).all()
    q3_answers = db.session.query((Answers.q3), func.count(Answers.id)).group_by(Answers.q3).all()
    labels3 = [q3_answers[i][0] for i in range(len(q3_answers))]
    values3 = [q3_answers[i][1] for i in range(len(q3_answers))]

    all_info['q4_mean'] = db.session.query(Answers.q4).all()
    q4_answers = db.session.query((Answers.q4), func.count(Answers.id)).group_by(Answers.q4).all()
    labels4 = [q4_answers[i][0] for i in range(len(q4_answers))]
    values4 = [q4_answers[i][1] for i in range(len(q4_answers))]

    all_info['q5_mean'] = db.session.query(Answers.q5).all()
    q5_answers = db.session.query((Answers.q5), func.count(Answers.id)).group_by(Answers.q5).all()
    labels5 = [q5_answers[i][0] for i in range(len(q5_answers))]
    values5 = [q5_answers[i][1] for i in range(len(q5_answers))]

    return render_template('results.html', all_info=all_info, set1=zip(values1, labels1, colours), set2=zip(values2, labels2, colours), set3=zip(values3, labels3, colours), set4=zip(values4, labels4, colours), set5=zip(values5, labels5, colours))


if __name__ == '__main__':
    app.run()