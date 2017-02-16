from flask import *
import MySQLdb
import os
import hashlib

def encrypt_password(password, username):
    result = hashlib.sha256(password + username).hexdigest()
    return result
    
def connect_db():
    db=MySQLdb.connect("localhost","root","123456","test")
    return db

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456' 
app.secret_key = "123456"

def init_db():
    db = connect_db()
    db.cursor().execute("drop table if exists user")
    db.cursor().execute("drop table if exists user_info")
    db.cursor().execute("create table user(username varchar(10),password varchar(100) not null,PRIMARY KEY(username));")
    db.cursor().execute("create table user_info(username varchar(10),sex char,email varchar(30),height smallint,weight smallint,BMI real,PRIMARY KEY(username));")
    db.commit()

init_db()

@app.route('/')
@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == 'POST':
        db = connect_db()
        cur = db.cursor()
        if not request.form.get('username') == None:
            u = request.form['username']
            p= encrypt_password(request.form['password'],u)
            bmi = 10000*int(request.form.get('weight'))/(int(request.form.get('height'))*int(request.form.get('height')))
            cur.execute('insert into user values (%s, %s)',(u,p))
            cur.execute('insert into user_info (username, email, sex, height, weight, BMI) values (%s, %s, %s, %s, %s, %s)',[request.form.get('username'),request.form.get('email'),request.form.get('sex'),request.form.get('height'),request.form.get('weight'),bmi])
            db.commit()
        flash('New users was successfully posted')
        return redirect(url_for('login'))


@app.route('/show',methods=['GET','POST'])
def show():
    db = connect_db()
    cur = db.cursor()
    count = cur.execute('select * from user')
    cur.execute('select * from user_info')
    result = [dict(username=row[0], sex=row[1], email=row[2], height=row[3], weight=row[4], bmi=row[5]) for row in cur.fetchall()]
    return render_template('show_users.html', result=result)

class loginError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

@app.route('/login', methods=['GET','POST'])
def login():
    db = connect_db()
    cur = db.cursor()
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        try:
            cur.execute("SELECT username FROM user WHERE username = %s",(u,))
            if not cur.fetchone():
                raise loginError('wrong username!')
            cur.execute('SELECT password FROM user WHERE username = %s',(u,))
            password = cur.fetchone()[0]
            if encrypt_password(p,u) == password:
                return redirect(url_for('show'))
            else:
                raise loginError('wrong password')
        except loginError as e:
            return render_template('login.html',error=e.value)

@app.route('/update', methods=['GET','POST'])
def update():
    db = connect_db()
    cur = db.cursor()
    if request.method == 'GET':
        return render_template("update.html")
    if request.method == 'POST':
        u = request.form['username']
        op = request.form['password']
        np = request.form['new_password']
        e = request.form['email']
        h = request.form['height']
        w = request.form['weight']
        try:
            cur.execute("SELECT username FROM user WHERE username = %s",(u,))
            if not cur.fetchone():
                raise loginError('wrong username!')
            cur.execute('SELECT password FROM user WHERE username = %s',(u,))
            password = cur.fetchone()[0]
            if encrypt_password(op,u) == password:
                cur.execute('UPDATE user_info SET email = %s WHERE username = %s',(e,u))
                p = encrypt_password(np,u)
                cur.execute('UPDATE user SET password = %s WHERE username = %s',(p,u))
                cur.execute('UPDATE user_info SET height = %s WHERE username = %s',(h,u))
                cur.execute('UPDATE user_info SET weight = %s WHERE username = %s',(w,u))
                db.commit()
                return redirect(url_for('show'))
            else:
                raise loginError('wrong password')
        except loginError as e:
        	return render_template('update.html',error=e.value)

@app.route('/delete', methods=['GET','POST'])
def delete():
    db = connect_db()
    cur = db.cursor()
    if request.method == 'GET':
        return render_template("delete.html")
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        try:
            cur.execute("SELECT username FROM user WHERE username = %s",(u,))
            if not cur.fetchone():
                raise loginError('wrong username!')
            cur.execute('SELECT password FROM user WHERE username = %s',(u,))
            password = cur.fetchone()[0]
            if encrypt_password(p,u) == password:
                cur.execute('DELETE FROM user WHERE username = %s',(u,))
                cur.execute('DELETE FROM user_info WHERE username = %s',(u,))
                db.commit()
                return redirect(url_for('show'))
            else:
                raise loginError('wrong password')
        except loginError as e:
            return render_template('delete.html',error=e.value)

@app.route('/unhealthy', methods=['GET','POST'])
def show_unhealthy():
    db = connect_db()
    cur = db.cursor()
    cur.execute('select * from user_info where BMI not between 18.5 and 24')
    result = [dict(username=row[0], sex=row[1], email=row[2], height=row[3], weight=row[4], bmi=row[5]) for row in cur.fetchall()]
    return render_template('show_unhealthy.html', result=result)

    
app.run(debug = True)