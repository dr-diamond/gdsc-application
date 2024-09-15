import os, hashlib
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')

#Def password hash function
def hash(password): 
    enc_password = password.encode('utf-8')
    hash_object = hashlib.sha256(enc_password)
    hashed_password = hash_object.hexdigest()
    return hashed_password


#Config user database, initialise sql, define user model
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

with app.app_context():
    db.create_all()

#Serve homepage
@app.route('/')
def index():
    #Check for messages signup/login success message
    success_message = request.args.get('message')
    username = session.get('username')
    return render_template('index.html', username=username)

# Route to handle the signup submission
@app.route('/submit_signup', methods=['POST'])
def submit_signup():
    # Capture form data
    username = request.form['username']
    password = request.form['password']
    #Check to see if the username already exists
    existing_user = User.query.filter(func.lower(User.username) == func.lower(username)).first()
    if existing_user:
        flash('Username already exists.')
        return redirect(url_for('signup'))
    # Hash password
    hashed_password = hash(password)
    #Commit new user to database
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    #Save username in session
    session["username"] = username
    #flash welcome message, redirect to home    
    return redirect(url_for('index'))

@app.route('/submit_login', methods=['POST'])
def submit_login():
    # Capture form data
    username = request.form['username']
    password = request.form['password']
    # Check if the user exists in the database
    user = User.query.filter_by(username=username).first()
    if user:
        # Hash the entered password
        hashed_password = hash(password)
        # Check if the hashed password matches the stored hash
        if user.password == hashed_password:
            # Store username in session
            session['username'] = user.username
            flash(f"Welcome back, {user.username}!")
            return redirect(url_for('index'))
        else:
            flash('Incorrect password. Please try again.', 'error')
    else:
        flash('Username does not exist.', 'error')

    # Redirect to the login page if authentication fails
    return redirect(url_for('login'))


#Serve signup page
@app.route('/signup')
def signup():
    return render_template('signup.html')

#Serve login page
@app.route('/login')
def login():
    return render_template('login.html')

#Serve logout page
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
