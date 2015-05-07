__author__ = 'Ken W. Alger'

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome to the Flask based Treehouse Leaderboard Site'


if __name__ == '__main__':
    app.run()
