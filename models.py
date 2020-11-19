from database import db
from crypto import Crypto

crypt = Crypto()

class Note(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))

    def __init__(self, title, text, date):
        self.title = title
        self.text = text
        self.date = date


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(200))

    def __init__(self, name, email, password):
        self.user_name = name
        self.email = crypt.encrypt(email)
        self.password = crypt.encrypt(password)

    def toString(self):
        print("\nUser: ")
        print("----------")
        print("id: " + str(self.id))
        print("user_name: " + str(self.user_name))
        print("email: " + str(self.email))
        print("password: " + str(self.password))
        print("\n")

class Comment(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    parent_id = db.Column("parent_id", db.Integer) #ID of note comment belongs to


    def __init__(self,text,date,parent):
        self.text = text
        self.date = date
        self.parent_id = parent
    
