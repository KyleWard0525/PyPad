# This is the flask python file that will serve and handle
# the note list page
import os
from flask import Flask
from flask import render_template

#Create flask app
app = Flask(__name__)

#Create an app route to serve the note_list.html page
@app.route("/note_list")
def note_list():
    return render_template("note_list.html")


#Run the app
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)