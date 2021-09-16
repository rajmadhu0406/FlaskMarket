from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/products")
def products():
    return "<p>This is products page!</p>"

@app.route('/user/<name>')
def user(name):
 return '<h1>Hello, %s!</h1>' % name


if(__name__ == "__main__"):
    app.run(debug=True, port=5000)