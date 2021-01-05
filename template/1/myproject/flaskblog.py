#create Flask instance
from flask import Flask
app = Flask(__name__)


@app.route("/")

#home page
@app.route("/home")
def home():
    return "<h1>Home Page</h1>"

#register page
@app.route("/register")
def about():
    return "<h1>Registration</h1>"


#enable debugging
if __name__ == '__main__':
    app.run(debug=True)   