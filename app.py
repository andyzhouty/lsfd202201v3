from flask import Flask, render_template, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
#     "mysql+pymysql://root:Ztymysql18@localhost:3306/classmates")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

article_list = (open(''.join([os.getcwd(), "/static/articles.txt"])).read().
            split('\n\n'))
article_double_list = []
for article in article_list:
    article_double_list += article.split('---')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', index=True)

@app.route('/main')
def main():
    return render_template('main.html', index=False)

@app.route('/members')
def members():
    return render_template('members.html', index=False)

@app.route('/articles')
@app.route('/articles/<id>')
def articles(id='1'):
    return render_template('articles.html', 
                           index=False,
                           article_title=article_double_list[2*int(id)-2],
                           article_content=article_double_list[2*int(id)-1],
                           enumerate_items=enumerate(article_list, start=1))

@app.route('/video')
def video():
    return render_template('video.html')
