from flask import *
import MySQLdb

def connect_db():
    db=MySQLdb.connect("localhost","root","123456","test")
    return db

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456' 
app.secret_key = "123456"

def test():
    db = connect_db()
    cur = db.cursor()
    count = cur.execute('select * from users')
    cur.execute('select * from users')
    result = [dict(id=row[0], password=row[1]) for row in cur.fetchall()]
    for i in result:
        print i.id

import os
import hashlib
def encrypt_password(password, username):
    result = hashlib.sha256(password + username).hexdigest()
    return result
    
def init_db():
    db = connect_db()
    db.cursor().execute("create table user(username varchar(10),password varchar(9) not null,PRIMARY KEY(username));")
    db.cursor().execute("create table user_info(username varchar(10),sex char,email varchar(10),PRIMARY KEY(username));")
    db.commit()

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
    db = connect_db()
    cur = db.cursor()
    if not request.form.get('username') == None:
        u = request.form['username']
        p,s = encrypt_password(request.form['password'])
        cur.execute('insert into user values (%s, %s, %s)',(u,p,s))
        cur.execute('insert into user_info (username, email, sex) values (%s, %s, %s)',[request.form.get('username'),request.form.get('email'),request.form.get('sex')])
        db.commit()
    flash('New users was successfully posted')
    return render_template("register.html")

p = encrypt_password('111','wcd')
print p
