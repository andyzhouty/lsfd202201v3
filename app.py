from flask import Flask, render_template, url_for, redirect, request
import os, pprint
app = Flask(__name__)

file_name = os.getcwd() + "/static/articles.txt"

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
        article_splited = article.split("-")
        for n, i in enumerate(["Title", "Author", "Content"]):
            article_full_dict.setdefault(i, [])
            article_full_dict[i].append(article_splited[n])

set_article_full_dict()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', navbar=False, warning=False)

@app.route('/main')
def main():
    return render_template('main.html', navbar=True, warning=True)

@app.route('/members')
def members():
    return render_template('members.html', navbar=True, warning=True)

@app.route('/articles')
@app.route('/articles/<id>')
def articles(id='1'):
    set_article_full_dict()
    return render_template('articles.html', 
                           navbar=True, warning=True,
                           article_title=article_full_dict["Title"][int(id)-1],
                           article_author=article_full_dict["Author"][int(id)-1],
                           article_content=article_full_dict["Content"][int(id)-1],
                           enumerate_items=enumerate(article_list, start=1))

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/upload')
def upload():
    return render_template('upload.html', navbar=False, warning=False)

@app.route('/upload-result', methods=['POST'])
def upload_result():
    global article_full_dict
    title = request.form['title']
    name = request.form['name']
    content = request.form['content']
    with open(file_name, "a") as file_obj:
        file_obj.write(f'\n{title}-{name}-{content}=\n')
    return render_template('upload_result.html')
