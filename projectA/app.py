from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def helloW(name=None):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

#clear
# git credential reject / git credential reject https://github.com