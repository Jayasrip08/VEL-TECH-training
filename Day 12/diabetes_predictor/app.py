from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

import sqlite3

app = Flask(__name__)

# DATABASE INITIALIZATION
def init_db():

    conn = sqlite3.connect("diabetes.db")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS predictions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        age INTEGER,

        glucose REAL,

        bmi REAL,

        risk TEXT

    )
    """)

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/assessment')
def assessment():
    return render_template('assessment.html')


@app.route('/predict', methods=['POST'])
def predict():

    name = request.form['name']
    age = request.form['age']
    glucose = float(request.form['glucose'])
    bmi = float(request.form['bmi'])

    # DUMMY LOGIC

    if glucose > 140 or bmi > 30:
        risk = "High Risk"

    elif glucose > 100:
        risk = "Moderate Risk"

    else:
        risk = "Low Risk"

    conn = sqlite3.connect("diabetes.db")

    conn.execute(
        '''
        INSERT INTO predictions
        (name,age,glucose,bmi,risk)

        VALUES (?,?,?,?,?)
        ''',
        (name,age,glucose,bmi,risk)
    )

    conn.commit()
    conn.close()

    return render_template(
        'result.html',
        name=name,
        risk=risk,
        glucose=glucose,
        bmi=bmi
    )


@app.route('/history')
def history():

    conn = sqlite3.connect("diabetes.db")

    data = conn.execute(
        "SELECT * FROM predictions ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        'history.html',
        data=data
    )


if __name__ == '__main__':
    app.run(debug=True)