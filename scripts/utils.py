import sys
import time
import re

special_chars = "!@#$%&_=./\()*^-+{}:;<>|[]`~"

"""
Function to validate password strength

Requirements:

1) 8 characters minimum
2) At least 1 capital letter
3) At least 1 lower-case letter
4) At least 1 special character
5) At least 1 number
"""
def checkPasswordStrength(password):

    global special_chars

    reply = "OK"

    #Strip password of any whitespaces
    password.replace(" ", "")

    #Digit, lower-case, upper-case, special char
    regex_rules = [r'\d', r'[a-z]', r'[A-Z]', "[!@#$%&_*()<>/\.^;:']"]

    #Check strength reqs.
    reqs_met = []
        


    #Loop through and search for regex
    for i in range(len(regex_rules)):
        reqs_met.append(re.search(regex_rules[i], password))

        #Requirement not met
        if reqs_met[i] == None:

            #Check which requirement wasn't met
            req_errs = {
                
                0 : "Password must contain at least 1 digit!",
                1 : "Password must contain at least 1 lower-case character!",
                2 : "Password must contain at least 1 upper-case character!",
                3 : "Password must contain at least 1 special character(!#*$@%^..)!"

                }
            #Set reply
            reply = req_errs[i]

    

    #Check length req.
    if len(password) < 8:
        reply = "Password must be at least 8 characters!"
    
    return reply

                 

    
