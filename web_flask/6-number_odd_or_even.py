#!/usr/bin/python3

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def home():
    return "Hello HBNB!!"

@app.route("/hbnb")
def hbnb():
    return "HBNB"

@app.route("/c/<text>", strict_slashes=False)
def c(text):
    text = text.replace("_", " ")
    return "C {}".format(text)

@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is_cool"):
    text = text.replace("_", " ")
    return "python {}".format(text)

@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    return "{:d} is an integer".format(n)

@app.route("/number_template/<int:n>")
def number_template(n):
    return render_template("5-number.html", content=n)

@app.route("/number_odd_or_even/<int:n>")
def number_odd_or_even(n):
    return render_template("6-number_odd_or_even.html", content=n)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
