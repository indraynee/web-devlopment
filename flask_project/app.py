from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

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
        errors['email'] = 'email id is required.'
    if not form_data.get('password'):
        errors['password'] = 'password is required'
    
    
    return errors

@app.route('/')
def index():
    return render_template('landingpage.html')

@app.route('/about_us.html')
def about():
    return render_template('about_us.html')

@app.route('/loginpage.html' , methods=['GET', 'POST'])
def login():
    errors = {}
    if request.method == 'POST':
        form_data = request.form
        errors = validate_login_form(form_data)
        if not errors:
            # If there are no validation errors, you can process the form data here
            # For example, you can save it to a database
            return redirect(url_for('index'))  # Redirect to homepage after successful signup
    # Pass the errors dictionary to the template
    return render_template('loginpage.html', errors=errors)

@app.route('/sign_up.html', methods=['GET', 'POST'])
def signup():
    errors = {}
    if request.method == 'POST':
        form_data = request.form
        errors = validate_signup_form(form_data)
        if not errors:
            # If there are no validation errors, you can process the form data here
            # For example, you can save it to a database
            return redirect(url_for('index'))  # Redirect to homepage after successful signup
    # Pass the errors dictionary to the template
    return render_template('sign_up.html', errors=errors)


if __name__ == '__main__':
    app.run(debug=True)
