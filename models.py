from database import db
from crypto import Crypto

crypt = Crypto()

class Note(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    comments = db.relationship("Comment", backref="note", cascade="all, delete-orphan", lazy=True)

    def __init__(self, title, text, date, user_id):
        self.title = title
        self.text = text
        self.date = date
        self.user_id = user_id

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(200))
    notes = db.relationship("Note", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)

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

    def getPW(self):
        return self.password

    def getEmail(self):
        return self.email

class Comment(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    text = db.Column("text", db.String(100))
    date = db.Column("date", db.String(50))
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    def __init__(self,text,date,note_id,user_id):
        self.text = text
        self.date = date
        self.parent_id = parent
        self.note_id = note_id
        self.user_id = user_id
