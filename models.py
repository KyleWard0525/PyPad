from database import db
from crypto import Crypto

crypt = Crypto()

class Note(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(200))
    text = db.Column("text", db.String(100))
    date = db.Column("data", db.String(50))

    def __init__(self, title, text, date):
        self.title = title
        self.text = text
        self.date = date

class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column("password", db.String(200))

    def __init__(self, name, email, password):
        self.name = name
        self.email = crypt.encrypt(email)
        self.password = crypt.encrypt(password)

    def toString(self):
        print("\nUser: ")
        print("----------")
        print("ID: " + str(self.id))
        print("Name: " + str(self.name))
        print("Email: " + str(self.email))
        print("Password: " + str(self.password))

def main():
    ted = User("ted", "ted@gmail.com", "ted's password")
    ted.toString()

main()
