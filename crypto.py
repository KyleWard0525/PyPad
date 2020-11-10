from cryptography.fernet import Fernet #pip install cryptography to access
import os

class Crypto:

    #Creates or reads encryption key
    def getKey(self):
        #Generate new key if none exists
        if not os.path.exists("crypto.key"):
            key_file = open("crypto.key", "wb")
            key = Fernet.generate_key()
            key_file.write(key)

            #Hide key file
            os.system("atrrib +H crypto.key")
            print("New key generated!")
            return key
        
        #Read in key from file
        else:
            key_file = open("crypto.key", "rb")
            key = key_file.read()
            print("Key read in from file!")
            return key


    def __init__(self):
        #Read in encryption key
        self.key = self.getKey()

    
    #Encrypt data
    def encrypt(self, data):
        #Create Fernet object
        f = Fernet(self.key)

        #Return encrypted data
        return f.encrypt(str.encode(data))

    #Decrypt data
    def decrypt(self, data):
        #Create Fernet object
        f = Fernet(self.key)

        #Return decrypted data
        return f.decrypt(data).decode()

