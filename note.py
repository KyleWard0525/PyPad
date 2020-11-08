# This is the flask python file that will be used to control server-side operations
import os
from flask import Flask
from flask import render_template
from datetime import date #Used to acquire today's date

#Create flask app
app = Flask(__name__)

"""
Create an app route to serve the note<noteid>.html page

Notes will contain the following information:
1) Title
2) Text
3) Date created / Last modified
4) Comments
"""
@app.route("/note/note_id")
def note(note_id):
    notes = { 0: {"title":"First note","text":"This really do be the first note",
                  "date":date.today(),"comments": []},
              1: {"title":"Second note","text":"Wait there's 2 notes?",
                  "date":date.today(),"comments": []},
              2: {"title":"Third note","text":"Hold on what's happening?!",
                  "date":date.today(),"comments": []}}
    render_template("note.html", note=notes[(int)note_id])

#Run the app
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
