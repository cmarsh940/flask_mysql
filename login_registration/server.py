from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
import os, binascii
import md5

app = Flask(__name__)
app.secret_key="Secret"
mysql = MySQLConnector(app,'login/register')


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#Homepage
@app.route('/')
def index():
    return render_template('index.html')

#Registration page
@app.route('/register')
def register():
    return render_template('register.html')
    
#Action for submitting registration form
@app.route('/handle_registration', methods=['POST'])
def handle_registration():
    passed = True
    query = "INSERT INTO users (first_name, last_name, username, email, password, salt, created_at, updated_at) VALUES (:first_name, :last_name, :username, :email, :hashed_pw, :salt, NOW(), NOW())"
    data = {}

#first_name validation
    if len(request.form['first_name']) > 1 and len(request.form['first_name']) < 51:
        data["first_name"] = request.form['first_name']
    else:
        flash("First name must be at least 2 characters!")
        passed = False

#last_name validation
    if len(request.form['last_name']) > 1 and len(request.form['last_name']) < 51:
        data["last_name"] = request.form['last_name']
    else:
        flash("Last name must be at least 2 characters!")
        passed = False

#username validation
    if len(request.form['username']) > 1:
        data["username"] = request.form['username']
    else:
        flash("Must enter username!")
        passed = False

#email validation
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
        passed = False
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        passed = False
    else:
        data["email"] = request.form['email']

#password validation
    if len(request.form['password']) < 8:
        flash("Password must be at least 8 characters long.")
        passed = False
    elif request.form['password'] != request.form['confirm_password']:
        flash("Passwords do not match.")
        passed = False
    else:
        password = request.form['password']
        salt = binascii.b2a_hex(os.urandom(15))
        hashed_pw = md5.new(password + salt).hexdigest()
        data['salt'] = salt
        data['hashed_pw'] = hashed_pw

    if passed:
        user_id = mysql.query_db(query, data)
        flash("Successfully registered!")
        session['id'] = user_id
        return redirect('/success')
    else:
        return redirect('/register')

#Login page
@app.route('/login')
def login():
    return render_template('login.html')

#Action for submitting login
@app.route('/handle_login', methods=['POST'])
def handle_login():
    username = request.form['username']
    password = request.form['password']
    user_query = "SELECT users.id, users.username, users.password, users.salt FROM users WHERE users.username = :username LIMIT 1"
    query_data = {'username': username}


    user = mysql.query_db(user_query, query_data)
    print "Printing data from login", user
    if len(user) != 0:
        test_password = md5.new(password + user[0]['salt']).hexdigest()
        print user[0]['password']
        print test_password
        if user[0]['password'] == test_password:
            flash("Successfully logged in!")
            session['id'] = user[0]['id']
            return redirect('/success')
        else:
            flash("Invalid login password. Please try again.")
            return redirect('/login')
    else:
        flash("Username not in database. Try again.")
        return redirect('/login')
#Success Page
@app.route('/success')
def success():
    #only displays if logged in 
    if not session['id']:
        return redirect('/login')
    else:
        return render_template('success.html')
app.run(debug=True)