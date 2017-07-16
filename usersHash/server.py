from flask import Flask, render_template, request, redirect, flash, session
from datetime import datetime #import for birthday
from mysqlconnection import MySQLConnector
import re #Regular Expression 
import md5

app = Flask(__name__)
app.secret_key = 'Secret'
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#Define routes

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/users/create', methods=['POST'])
def create_user():
     username = request.form['username']
     email = request.form['email']
     password = md5.new(request.form['password']).hexdigest();
     insert_query = "INSERT INTO users (username, email, password, created_at, updated_at) VALUES (:username, :email, :password, NOW(), NOW())"
     query_data = { 'username': username, 'email': email, 'password': password }
     mysql.query_db(insert_query, query_data)

@app.route('/submit', methods=['POST'])
def createuser():
    invalid = False
    if len(request.form['firstname']) < 1:
        flash("You must enter your first name")
        invalid = True

    if len(request.form['lastname']) < 1:
        flash("You must enter your last name")
        invalid = True

    if request.form['firstname'].isalpha() == False or request.form['lastname'].isalpha() == False:
        flash("First and Last name must not contain any numbers.")
        invalid = True

    if len(request.form['email']) < 1:
        flash("Email must be entered")
        invalid = True

    elif not email_regex.match(request.form['email']):
        flash('Invalid Email Address')
        invalid = True

    if len(request.form['password']) < 1:
        flash("Password must be entered")
        invalid = True

    if len(request.form['password']) < 8:
        flash("Password should be at least 8 characters")
        invalid = True

    num = 0
    for i in request.form['password']:
        if i.isnumeric() == True:
            num += 1

    if num == 0:
        flash("Your password must have at least 1 number")
        invalid = True

    topnum = 0
    for i in request.form['password']:
        if i.isupper() == True:
            topnum += 1

    if topnum == 0:
        flash("Your password must have at least 1 capital letter")
        invalid = True

    if len(request.form['pwconfirm']) < 1:
        flash("You must confirm your password")
        invalid = True

    if request.form['password'] != request.form['pwconfirm']:
        flash("Password and password confirm should match")
        invalid = True

    birthdate = datetime.strptime(request.form['bday'],'%Y-%m-%d')
    if birthdate >= datetime(2017,07,20):
        flash("Birthdate must be before that date")
        invalid = True

    if invalid:
        return redirect('/')

    else:
        flash("You have successfully registered.")
        return redirect('/')

app.run(debug=True) #run server