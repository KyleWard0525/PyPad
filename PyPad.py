# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
import sys
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import Note as Note
from models import User as User
from crypto import Crypto
from datetime import date

#Load /scripts into sys path
sys.path.insert(1, "/scripts")

from scripts import utils

app = Flask(__name__)

crypt = Crypto() #For encrypting/decrypting data

#Create database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

#Disable tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Connect the database object to the flask app
db.init_app(app)

#Current logged-in user
curr_user = None

#Mock notes
mock_notes = {

    0 : {"title": "First note", "text": "First note text", "date":date.today().strftime("%m-%d-%Y")},
    1 : {"title": "Second note", "text": "Second note text", "date":date.today().strftime("%m-%d-%Y")},
    2 : {"title": "Third note", "text": "Third note text", "date":date.today().strftime("%m-%d-%Y")}
    }

#Setup models
with app.app_context():
    db.create_all() #run under app context

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')
def index():    

    #Print out all users in the database
    users = User.query.all()

    for user in users:
        user.toString()

        if user.user_name == "Not Kyle Ward":
            print("\nUser: Not Kyle Ward:\n")
            print("Email: " + str(crypt.decrypt(user.email)))
            print("Password: " + str(crypt.decrypt(user.password)))

    return render_template('index.html', user = curr_user)

@app.route('/notes')
def get_notes():

    my_notes = mock_notes

    return render_template('notes.html', notes=my_notes, user = curr_user)

@app.route('/notes/<note_id>')
def get_note(note_id):

    my_notes = db.session.query(Note).filter_by(id=note_id).one()

    return render_template('note.html', note=my_notes, user = curr_user)

@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
        if request.method == 'POST':

            title = request.form['title']

            text = request.form['noteText']

            
            today = date.today()
            today = today.strftime("%m-%d-%Y")
            new_record = Note(title, text, today)
            db.session.add(new_record)
            db.session.commit()

            return redirect(url_for('get_notes'))

        else:
            return render_template('new.html', user=curr_user)
#App route to edit note
@app.route('/notes/edit/<note_id>', methods=["GET", "POST"])
def update_note(note_id):

    #Check for POST request
    if request.method == "POST":
        title = request.form['title']
        text = request.form['noteText']
        note = db.session.query(Note).filter_by(id=note_id).one()

        #Update note data
        note.title = title
        note.text = text

        #Update database
        db.session.add(note)
        db.session.commit()

        return redirect(url_for('get_notes'))
    else:
        #Get note with note_id from db
        my_note = db.session.query(Note).filter_by(id=note_id).one()

        return render_template('new.html', note=my_note, user=curr_user)

#Create account page
@app.route('/createAccount', methods=["GET", "POST"])
def createAccount():
    
    #Check request type
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        pw = request.form['password']

        #Check password requirements
        if not utils.checkPasswordStrength(pw) == "OK":
            return render_template("createAccount.html", error=utils.checkPasswordStrength(pw))

        #Encrypt data and create user object
        user = User(name=username,email=email,password=pw)

        user.toString()

        
        #Check if user email already exists
        if db.session.query(User).filter_by(email=email).first():
            return render_template("createAccount.html", error="Email already in use!")
        #Check if username is already in use
        elif db.session.query(User).filter_by(user_name = user.user_name).first():
            return render_template("createAccount.html", error="Username already in use!")
        else:
            #Add user to databse
            db.session.add(user)
            db.session.commit()

            #Set current user
            curr_user = user
            return render_template("index.html", user=curr_user)
        

    return render_template("createAccount.html", error="")

#User login
@app.route('/login', methods=["GET", "POST"])
def login():

    #User is attempting to login
    if request.method == "POST":
        email = request.form['email']
        pw = request.form['password']

        #Encrypted login data and make User object
        email = crypt.encrypt(email)
        pw = crypt.encrypt(pw)
        user = User(name="", email=email, password=pw)

        #Check email exists
        if db.session.query(User).filter_by(email=email).first():
            #Check if password is correct
            user = db.session.query(User).filter_by(email=email).one()

            #Passwords match
            if user.getPW() == pw:
                #Return to homepage
                curr_user = user
                return render_template("index.html", user=user)
            
            #Wrong password
            else:
                return render_template("login.html", error="Incorrect password!")
        else:
            #User email not found
            return render_template("login.html", error="Email not found!")

    return render_template("login.html", error="")

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.

