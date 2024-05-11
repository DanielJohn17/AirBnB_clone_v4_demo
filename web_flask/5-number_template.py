#!/usr/bin/python3

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/<int:n>")
def home(n):
    return render_template("5-number.html", content=n)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
