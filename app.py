from flask import Flask, request, render_template, g, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'comments.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    comment_text = request.form['comment'].strip().lower()  # Normalize input text
    db = get_db()
    
    # Perform a case-insensitive search in the database
    cur = db.execute("SELECT deceptive FROM comments WHERE LOWER(TRIM(text)) = ?", (comment_text,))
    result = cur.fetchone()
    
    if result:
        deceptive = result[0]
        prediction = 'Not a Spam' if deceptive == 'truthful' else 'Spam'
    else:
        prediction = 'Comment not found in the database'

    return render_template('index.html', prediction=prediction, comment=request.form['comment'])

@app.route('/comments')
def comments():
    db = get_db()
    cur = db.execute('SELECT * FROM comments')
    entries = cur.fetchall()
    return render_template('comments.html', entries=entries)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    deceptive = request.form['deceptive']
    hotel = request.form['hotel']
    polarity = request.form['polarity']
    source = request.form['source']
    text = request.form['text'].strip().lower()  # Normalize text input
    
    db = get_db()
    db.execute('INSERT INTO comments (deceptive, hotel, polarity, source, text) VALUES (?, ?, ?, ?, ?)',
               (deceptive, hotel, polarity, source, text))
    db.commit()
    
    return redirect(url_for('index'))

@app.route('/user')
def user():
    return render_template('user.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

