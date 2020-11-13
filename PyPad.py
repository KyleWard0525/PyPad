# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running

# imports
import os                 # os is used to get environment variables IP & PORT
from flask import Flask   # Flask is the web app that we will customize
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import Note as Note
from models import User as User
from crypto import Crypto

app = Flask(__name__)

crypt = Crypto() #For encrypting/decrypting data

#Create database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

#Disable tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    a_user = db.session.query(User).filter_by(email='ysong21@uncc.edu').one()

    return render_template('index.html', user = a_user)

@app.route('/notes')
def get_notes():

    a_user = db.session.query(User).filter_by(email='ysong21@uncc.edu').one()

    my_notes = db.session.query(Note).all()

    return render_template('notes.html', notes=my_notes, user = a_user)

@app.route('/notes/<note_id>')
def get_note(note_id):

    a_user = db.session.query(User).filter_by(email='ysong21@uncc.edu').one()

    my_notes = db.session.query(Note).filter_by(id=note_id).one()

    return render_template('note.html', note=my_notes, user = a_user)

@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
        if request.method == 'POST':

            title = request.form['title']

            text = request.form['noteText']

            from datetime import date
            today = date.today()
            today = today.strftime("%m-%d-%Y")
            new_record = Note(title, text, today)
            db.session.add(new_record)
            db.session.commit()

            return redirect(url_for('get_notes'))

        else:
            a_user = db.session.query(User).filter_by(email='ysong21@uncc.edu').one()
            return render_template('new.html', user=a_user)

#Create account page
@app.route('/create_account', methods=["GET", "POST"])
def create_account():
    #Check request type
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        pw = request.form['pw']

        #Encrypt data and create user object
        email = crypt.encrypt(email)
        pw = crypt.encrypt(pw)
        user = User(name,email,pw)

        #Check if user email already exists
        if db.session.query(User).filter_by(email=email).scalar() is None:
            return render_template("status.html")
        else:
            #Add user to databse
            db.session.add(user)
            db.session.commit()
            return render_template("status.html")

        return 'bad'


app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.

