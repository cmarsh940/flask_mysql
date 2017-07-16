from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector 
import re


app = Flask(__name__)
mysql = MySQLConnector(app,'emails')
app.secret_key = 'Secret'
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    query = "SELECT email FROM users"
    users = mysql.query_db(query)
    return render_template('success.html', users=users)

@app.route('/users/<user_id>')
def show(user_id):
    query = "SELECT users.email FROM users WHERE id = :specific_id"
    data = {'specific_id': user_id}
    users = mysql.query_db(query, data)
    return render_template('success.html', one_user=user[0])

@app.route('/create', methods=['POST'])
def create():
    if len(request.form['email']) < 1:
        flash("Email must be entered")
        invalid = True

    elif not email_regex.match(request.form['email']):
        flash('Invalid Email Address')
        invalid = True

    else:
        query = "INSERT INTO users (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {
             'email': request.form['email'],
        }
    mysql.query_db(query, data)
    return redirect('/success')

app.run(debug=True) (edited)
