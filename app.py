# -*- coding:utf-8 -*-
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import os, sys

app = Flask(__name__)
bootstrap = Bootstrap(app)

if sys.platform == "win32":
    # 本地运行
    file_name = os.getcwd() + "/static/articles.txt"
else:
    # PythonAnywhere 部署
    file_name = "/home/ls202201/mysite/static/articles.txt"

article_full_dict = dict()
article_list = []


def set_article_full_dict():
    global article_list
    global article_full_dict
    article_full_dict = dict()
    article_list = open(file_name, encoding="utf-8").read().strip().split('=')
    if not article_list[-1]:
        del article_list[-1]
    for article in article_list:
        if not article:
            break
        article_splited = article.split("`", 3)
        for n, i in enumerate(["Title", "Author", "Content"]):
            article_full_dict.setdefault(i, [])
            article_full_dict[i].append(article_splited[n])


set_article_full_dict()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/main')
def main():
    return render_template('main.html', warning=True)


@app.route('/members')
def members():
    return render_template('members.html', warning=True)


@app.route('/articles')
@app.route('/articles/<int:id>')
def articles(id=1):
    set_article_full_dict()
    return render_template('articles.html',
                           has_navbar=True, warning=True,
                           article_title=article_full_dict["Title"][id - 1],
                           article_author=article_full_dict["Author"][id - 1],
                           article_content=article_full_dict["Content"][id - 1],
                           enumerate_items=enumerate(article_list, start=1))


@app.route('/video')
def video():
    return render_template('video.html', warning=True)


@app.route('/upload')
def upload():
    return render_template('upload.html', warning=False)


@app.route('/upload-result', methods=['POST'])
def upload_result():
    title = request.form['title']
    name = request.form['name'].encode('utf-8').decode()
    print(name)
    content = request.form['content']
    password = request.form['password']
    if password != "LSFD202201":
        return render_template('upload_fail.html')
    with open(file_name, "a", encoding="utf-8") as file_obj:
        file_obj.write(f'\n{title}`{name}`{content}=\n')
    return render_template('upload_result.html')


@app.route('/kzkt')
def cloud_class():
    return render_template('kzkt.html', warning=True)


@app.route('/jkl')
def jkl():
    return render_template('jinkela.html', warning=False)


@app.errorhandler(404)
@app.route('/hrtg')
def page_not_found(e="hrtg"):
    return render_template('coffin_dance.html', warning=False), 404


@app.errorhandler(500)
@app.route('/mickey-aoligei')
def internal_server_error(e="aoligei"):
    return render_template('mickey_aoligei.html', warning=False), 500
