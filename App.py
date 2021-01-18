from flask import Flask, render_template, url_for, redirect, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] =""
app.config['MYSQL_DB'] = 'travel'

mysql = MySQL(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/blog_page', methods=['GET', 'POST'])
def blogs():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('travel_blogs.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('about.html')

@app.route('/signup', methods =['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'phone' in request.form and 'location' in request.form:
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        location = request.form['location']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE name = % s', (name, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'name must contain only characters !'
        elif not name or not password or not email:
            msg = 'FAILED Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, %s)', (name, password, email, phone, location ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'FAILED Please fill out the form !'
    return render_template('signup.html', msg = msg)

@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s AND password = % s', (email, password, ))
        accounts = cursor.fetchone()
        if accounts:
            session['loggedin'] = True
            # session['id'] = account['id']
            session['email'] = accounts['email']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect name / password !'
    return render_template('login.html', msg = msg)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name,email,phone) VALUES (%s,%s)", (name,email,phone))
        mysql.connection.commit()
        cur.close()

        return "success"
        #return redirect(url_for('index'))
    return render_template('contact.html')

#
if __name__ == '__main__':
   app.run(debug = True)