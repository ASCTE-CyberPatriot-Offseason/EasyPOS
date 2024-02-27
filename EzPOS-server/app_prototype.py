from flask import Flask
import flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'
print(help(flask.app))