#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def say_hello():
    """Displays message"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def say_HBNB():
    """Displays message"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_is_fun(text):
    """route with dynamic parameter"""
    return "C {}".format(text.replace("_", " "))


@app.route("/python/", defaults={"text":"is cool"}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_is_cool(text):
    """route with dynamic parameter with a default"""
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>")
def number(n):
    """route with dynamic parameter with a specific type""" 
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

