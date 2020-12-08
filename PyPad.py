# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
import sys
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for, session
from database import db
from datetime import date
from models import Note as Note
from models import User as User
from crypto import Crypto


#Load /scripts into sys path
sys.path.insert(1, "/scripts")

from scripts import utils

app = Flask(__name__)

crypt = Crypto() #For encrypting/decrypting data

#Create database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

#Disable tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Configure session key
app.config['SECRET_KEY'] = 'SE3155'

#Connect the database object to the flask app
db.init_app(app)

#Setup models
with app.app_context():
    db.create_all() #run under app context


# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')
def index():
    #Check if user exists
    if session.get('user'):       
        return render_template('index.html', user = session['user'])
    else:
        return render_template('index.html')

@app.route('/notes')
def get_notes():
    #Check if user exists
    if session.get('user'):
        #Get user notes
        user_notes = db.session.query(Note).filter_by(user_id=session['user_id'])
        return render_template('notes.html', notes=user_notes, user = session['user'])
    else:
        #Redirect to login page
        return redirect(url_for('login'))

    

@app.route('/notes/<note_id>')
def get_note(note_id):
    #Check if user exists
    if session.get('user'):
        #Get the current note
        user_note = db.session.query(Note).filter_by(id=note_id).one()
        return render_template('note.html', note=user_note, user = session['user'])
    else:
        return redirect(url_for('get_notes'))

    

#App route to view new note page
@app.route('/notes/new_note', methods=["GET", "POST"])
def new_note():
    
    if session.get('user'):
    #Check request method
        if request.method == "POST":
        #Process form data and add new note to list
            title = request.form["title"]
            text = request.form["noteText"]
            today = date.today().strftime("%m-%d-%Y")
        
        #Create new note and add to db
            new_record = Note(title, text, today, user_id = session['user_id'])
            db.session.add(new_record)
            db.session.commit()
        
        #Redirect user to view notes list
            return redirect(url_for("get_notes"))
        
        else:
            return render_template("new.html", user=session['user'])
    else:
        return redirect(url_for('login'))

#App route to delete a note
@app.route('/notes/delete/<note_id>', methods=["POST"])
def delete_note(note_id):
    if session.get('user'):
        
        #Get note from database
        user_note = db.session.query(Note).filter_by(id=note_id).one()

        #Delete note
        db.session.delete(user_note)
        db.session.commit()

        return redirect(url_for('get_notes'))
    else:
        return redirect(url_for('login'))

#App route to edit note
@app.route('/notes/edit/<note_id>', methods=["GET", "POST"])
def update_note(note_id):

    if session.get('user'):
        
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

            return render_template('new.html', note=my_note, user=session['user'])
    else:
        return redirect(url_for('login'))

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


        #create user object
        user = User(name=username,email=email,password=pw)

        
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

            #Save user's name
            session['user'] = user.user_name

            session['user_id'] = user.id
            
            return render_template("index.html", user=session['user'])
        

    return render_template("createAccount.html", error="")

#User login
@app.route('/login', methods=["GET", "POST"])
def login():

    #User is attempting to login
    if request.method == "POST":
        username = request.form['username']
        pw = request.form['password']

        #Make User object
        user = User(name=username, email="", password=pw)

        #Check user exists
        if db.session.query(User).filter_by(user_name=username).first():
            #Check if password is correct
            user = db.session.query(User).filter_by(user_name=username).one()

            #Passwords match
            if crypt.decrypt(user.getPW()) == pw:
                #Return to homepage
                session['user'] = user.user_name
                session['user_id'] = user.id
                return render_template("index.html", user=session['user'])
            
            #Wrong password
            else:
                return render_template("login.html", error="Incorrect password!")
        else:
            #User email not found
            return render_template("login.html", error="User not found!")

    return render_template("login.html", error="")

@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.

