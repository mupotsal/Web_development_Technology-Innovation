# Liberty Mupotsa
# Web development Projects
# Berea College
# This project is centred on creating a website for technology and innovation
# web development #





from flask import Flask, render_template,flash,url_for, sessions, logging


from flask import render_template
from data import Articles


app = Flask(__name__)

# @ is the decorator , its a way to wrap a function and wrap its behavior
Articles = Articles()
@app.route('/')
def index():


    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/articles')
def articles():
    return render_template("articles.html", articles = Articles)


@app.route('/articles/<string:id>/')
def article(id):
    return render_template("article.html", id= id )


# @app.route('/tuna') # You can create multiple pages but there is need of putting the decorator before.
# def tuna():
#     return '<h1> Tuna is good </h1>' \
#            '<h2> This is page 2 </h2>'
# @app.route('/profile/<username>')
# def profile(username):
#     return '<h2> Hey there %s </h2>' % username

if __name__ =="__main__"\
        :
    app.run(debug=True)
