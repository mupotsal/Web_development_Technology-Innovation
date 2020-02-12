# Liberty Mupotsa
# Web development Projects
# Berea College
# This project is centred on creating a website for technology and innovation
# web development #


from flask import *
from flask import Flask, render_template,flash,url_for, sessions, logging, request,redirect
from mysql import *
from mysql import connector
import pymysql
pymysql.install_as_MySQLdb()
from mysql_db import *
from wtforms import Form, StringField,TextAreaField,PasswordField,validators, form
from passlib.hash import sha256_crypt
from functools import wraps
from flask import render_template

app = Flask(__name__)

# @ is the decorator , its a way to wrap a function and wrap its behavior
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Usap2017'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Articles = Articles()
# Initialize MYSQL
mysql = MySQL(app)
@app.route('/')
def index():


    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/articles')
def articles():
    # Create cursor
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)


    # Get articles

# Close connection
    cur.close()


@app.route('/articles/<string:id>/')
def article(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article= cur.fetchone()

    return render_template('article.html', article=article)


class RegisterForm(Form):
    name = StringField('Name',[validators.length(min =1, max = 50)])
    username  = StringField('Username',[validators.length(min = 4, max = 25)])
    email = StringField('Email', [validators.length(min = 6, max= 50)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message = 'Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register',methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
    # create the cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name,  email, username, password) Values(%s, %s, %s, %s )",(name, email,username,password))
    # commit to DB
        mysql.connection.commit()

    # close connection

        cur.close()
        flash("You  are now registered and can login",'success')
        return redirect(url_for('index'))

        #return render_template('register.html',form= form)


    form = RegisterForm(request.form)
    return render_template('register.html',form= form)


# User ogin
@app.route('/login',methods= ['GET','POST'])
def login():
    if request.method == 'POST':
        #Get form fields
        username = request.form['username']
        password_candidate = request.form['password']

        #create cursor
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s",[username])
        if result > 0:
            data = cur.fetchone()

            password = data['password']
            #comapre passwords
            if sha256_crypt.verify(password_candidate,password):
                session ['logged_in'] = True
                session ['username'] = username
                flash ('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'

                return render_template('login.html', error=error)
        cur.close()
    else:
        error = 'Username not found'
        return render_template("login.html", error=error)
    return render_template('login.html')

#check if user logged i
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
             flash('Unauthorized, Please login','danger')
             return redirect (url_for('login'))
    return wrap
#Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("You are now logged out", "success")
    return redirect(url_for('login'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result > 0:
        return render_template('templates/dashboard.html', articles=articles)
    else:
        msg = 'No articles found'
        return render_template('templates/dashboard.html', msg=msg)

    cur.close()


class ArticleForm(Form):
    title = StringField('Title', [validators.length(min =1, max = 200)])
    body  = TextAreaField('Body',[validators.length(min = 30)])


# add article


@app.route('/add_article', methods = ['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        #create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)", (title,body,session['username']))
        mysql.connection.commit()

        cur.close()
        flash ('Article Created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('templates/add_article.html', form=form)

#Edit article
@app.route('/edit_article/<string:id>', methods = ['GET', 'POST'])
@is_logged_in
def edit_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    #Get article by the id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()
    cur.close()
    form = ArticleForm(request.form)
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

       #create cursor
        cur = mysql.connection.cursor()
        app.logger.info(title)
        cur.execute("UPDATE articles SET title=%s, body=%s WHERE id=%s", (title, body, id))
        mysql.connection.commit()
        cur.close()
        flash ('Article updated', 'success')
        return redirect(url_for('dashboard'))
    return render_template('templates/edit_article.html', form=form)

#delete article


@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM articles WHERE  id = %s",[id])
    mysql.connection.commit()
    cur.close()
    flash('Article deleted', 'success')
    return redirect(url_for('dashboard'))

# @app.route('/tuna') # You can create multiple pages but there is need of putting the decorator before.
# def tuna():

#     return '<h1> Tuna is good </h1>' \
#            '<h2> This is page 2 </h2>'
# @app.route('/profile/<username>')
# def profile(username):
#     return '<h2> Hey there %s </h2>' % username


if __name__ =="__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)
