from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_mail import Mail
import json
import os
import math
from datetime import datetime
from flaskext.mysql import MySQL


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'
# app.config['UPLOAD_FOLDER'] = params['upload_location']
# app.config.update(
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = '465',
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = params['gmail-user'],
#     MAIL_PASSWORD=  params['gmail-password']
# )
# mail = Mail(app)

# Database connection info. Note that this is not a secure connection.
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ""
app.config['MYSQL_DATABASE_DB'] = 'Mechanics'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:@localhost/mechanics"



if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


class Kworkers(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(11), nullable=False)
    phone_num = db.Column(db.String(14), nullable=False)
    garage_name = db.Column(db.String(30), nullable=False)


class Cworkers(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(11), nullable=False)
    phone_num = db.Column(db.String(14), nullable=False)
    garage_name = db.Column(db.String(30), nullable=False)


class Mworkers(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(11), nullable=False)
    phone_num = db.Column(db.String(14), nullable=False)
    garage_name = db.Column(db.String(30), nullable=False)


class Dworkers(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(11), nullable=False)
    phone_num = db.Column(db.String(14), nullable=False)
    garage_name = db.Column(db.String(30), nullable=False)


class Cities(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(10), nullable=False)
    pic = db.Column(db.String(500), nullable=False)


# @app.route("/")
# def home():
#     posts = Posts.query.filter_by().all()
#     last = math.ceil(len(posts)/int(params['no_of_posts']))
#     #[0: params['no_of_posts']]
#     #posts = posts[]
#     page = request.args.get('page')
#     if(not str(page).isnumeric()):
#         page = 1
#     page= int(page)
#     posts = posts[(page-1)*int(params['no_of_posts']): (page-1)*int(params['no_of_posts'])+ int(params['no_of_posts'])]
#     #Pagination Logic
#     #First
#     if (page==1):
#         prev = "#"
#         next = "/?page="+ str(page+1)
#     elif(page==last):
#         prev = "/?page=" + str(page - 1)
#         next = "#"
#     else:
#         prev = "/?page=" + str(page - 1)
#         next = "/?page=" + str(page + 1)



#     return render_template('index.html', params=params, posts=posts, prev=prev, next=next)



@app.route("/about")
def about():
    return render_template('about.html', params=params)


# @app.route("/dashboard", methods=['GET', 'POST'])
# def dashboard():

#     if ('user' in session and session['user'] == params['admin_user']):
#         posts = Posts.query.all()
#         return render_template('dashboard.html', params=params, posts = posts)


#     if request.method=='POST':
#         username = request.form.get('uname')
#         userpass = request.form.get('pass')
#         if (username == params['admin_user'] and userpass == params['admin_password']):
#             #set the session variable
#             session['user'] = username
#             posts = Posts.query.all()
#             return render_template('dashboard.html', params=params, posts = posts)

#     return render_template('login.html', params=params)



# login----------------------------------------------------------------------
@app.route("/login",methods=['GET','POST'])
def login():

    if request.method == "POST":
        name = request.form['name']
        password = request.form['pass']
        cursor.execute("SELECT * FROM `users` WHERE name='"+name+"' and password='"+password+"'")
        r=cursor.fetchall()
        count=cursor.rowcount

        if count==1:
            session['user'] = name

            return render_template('index2.html', params=params)
    return render_template('login.html', params=params)


# signup------------------------------------------------------------------------------------------------
@app.route("/signup",methods=['GET','POST'])
def signup():

    if request.method == "POST":
        name = request.form['name']
        password = request.form['Password']
        Cpassword = request.form['cPassword']
        if password==Cpassword:
            session['user'] = name
            cursor.execute("INSERT INTO `users` (`name`, `password`) Values (%s, %s)", (name, password))
            conn.commit()
            return render_template("index2.html", params=params)

    return render_template('signup.html')


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')


# @app.route("/contact", methods = ['GET', 'POST'])
# def contact():
#     if(request.method=='POST'):
#         name = request.form.get('name')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         message = request.form.get('message')
#         entry = Contacts(name=name, phone_num = phone, message = message, date= datetime.now(),email = email )
#         db.session.add(entry)
#         db.session.commit()
#         mail.send_message('New message from ' + name,
#                           sender=email,
#                           recipients = [params['gmail-user']],
#                           body = message + "\n" + phone
#                           )
#     return render_template('contact.html', params=params)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')





@app.route("/location", methods = ['GET', 'POST'])
def location():
    cities = Cities.query.filter_by().all()
    return render_template('location.html',cities=cities)    



@app.route("/repair/1")
def repair1():
    posts = Kworkers.query.filter_by().all()
    return render_template('repair2.html',posts=posts)
    
@app.route("/repair/2")
def repair2():
    posts = Mworkers.query.filter_by().all()
    return render_template('repair2.html',posts=posts)

@app.route("/repair/3")
def repair3():
    posts = Dworkers.query.filter_by().all()
    return render_template('repair2.html',posts=posts)

@app.route("/repair/4")
def repair4():
    posts = Cworkers.query.filter_by().all()
    return render_template('repair2.html',posts=posts)


app.run(debug=True)