from flask import Flask, request, session, redirect, url_for, render_template
import mysql.connector

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='a@',
    database='geeklogin'
)
cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) UNIQUE, password VARCHAR(255))")

@app.route('/')
def home():
    if 'username' in session:
        return f'Prijavljeni ste kao {session["username"]}<br><a href="/logout">Odjava</a>'
    return 'Niste prijavljeni<br><a href="/login">Prijava</a> ili <a href="/signup">Registracija</a>'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        account = cursor.fetchone()
        if account:
            return f'Profil već postoji.'
        else:
            return f'Profil uspešno napravljen'
            mysql.connector.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        return 'Pogrešno korisničko ime ili lozinka'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run(debug=True)
