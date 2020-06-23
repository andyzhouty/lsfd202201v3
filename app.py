from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', index=True)

@app.route('/main')
def main():
    return render_template('main.html', index=False)
