from flask import Flask, render_template, redirect, url_for
 
app = Flask(__name__)

@app.route('/')
def main():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')
 
app.run(host='localhost', port=5000)