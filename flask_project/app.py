from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('landingpage.html')

@app.route('/about_us.html')
def about():
    return render_template('about_us.html')

@app.route('/loginpage.html')
def login():
    return render_template('loginpage.html')

@app.route('/sign_up.html')
def signup():
    return render_template('sign_up.html')

if __name__ == '__main__':
    app.run(debug=True)
