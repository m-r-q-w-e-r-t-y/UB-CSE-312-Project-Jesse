from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/login",methods=['GET'])
def login():
    return render_template('login.html')

@app.route("/signup",methods=['GET'])
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True)