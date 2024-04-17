from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import re
import pymysql
from datetime import datetime

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask_project'
db = SQLAlchemy(app)

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Define the BlogPost model
# Define the BlogPost model with an explicit table name
class BlogPost(db.Model):
    __tablename__ = 'blogpost'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"BlogPost(title='{self.title}', content='{self.content}', image='{self.image}')"
# Function to perform server-side validation
def validate_signup_form(form_data):
    print("Validating form data...")
    errors = {}
    if not form_data.get('first_name'):
        errors['first_name'] = 'First name is required.'
    if not form_data.get('last_name'):
        errors['last_name'] = 'Last name is required.'
    if not form_data.get('email'):
        errors['email'] = 'Email is required.'
    elif not re.match(r'^[\w\.-]+@[\w\.-]+$', form_data.get('email')):
        errors['email'] = 'Invalid email format.'
    
    return errors

def validate_login_form(form_data):
    print("Validating form data...")
    errors = {}
    if not form_data.get('email'):
        errors['email'] = 'Email is required.'
    if not form_data.get('password'):
        errors['password'] = 'Password is required'
    
    return errors

@app.route('/landingpage.html')
def landing():
    return render_template('landingpage.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/post.html')
def post():
    return render_template('post.html')

@app.route('/about_us.html')
def about():
    return render_template('about_us.html')

@app.route('/loginpage.html', methods=['GET', 'POST'])
def login():
    errors = {}
    if request.method == 'POST':
        form_data = request.form
        errors = validate_login_form(form_data)
        if not errors:
            return redirect(url_for('index'))  
    return render_template('loginpage.html', errors=errors)

@app.route('/sign_up.html', methods=['GET', 'POST'])
def signup():
    errors = {}
    if request.method == 'POST':
        form_data = request.form
        errors = validate_signup_form(form_data)
        if not errors:
            # If there are no validation errors, save user data to the database
            new_user = User(first_name=form_data['first_name'], last_name=form_data['last_name'], email=form_data['email'])
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('landing'))  # Redirect to homepage after successful signup
    # Pass the errors dictionary to the template
    return render_template('sign_up.html', errors=errors)

@app.route('/create_blog', methods=['GET', 'POST'])
def create_blog():
    if request.method == 'POST':
        form_data = request.form
        new_blog = BlogPost(title=form_data['title'], content=form_data['content'], image=form_data['image'])
        db.session.add(new_blog)
        db.session.commit()
        # Redirect to the route for displaying new posts
        return redirect(url_for('new_posts'))
    return render_template('create_blog.html')

@app.route('/new_posts.html')
def new_posts():
    # Fetch all blog posts from the database
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()

    for post in posts:
        post.image_url = url_for('static', filename='post_img/' + post.image)
        
    return render_template('new_posts.html', posts=posts)


if __name__ == '__main__':
    app.run(debug=True)