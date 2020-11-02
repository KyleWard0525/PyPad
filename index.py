# This is the flask python file that will be used to control server-side operations
import os
from flask import Flask
from flask import render_template

#Create flask app
app = Flask(__name__)

#Create an app route to serve the index.html page
@app.route("/index")
def index():
    return render_template("index.html")


#Run the app
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)
