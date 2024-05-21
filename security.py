import base64
import string
from os import urandom
from argon2 import PasswordHasher

ph = PasswordHasher()

def emailValidator(emailStr:str)->bool:
    hasa = False
    hasp = False

    acceptableChars = set(string.ascii_lowercase + string.ascii_uppercase + string.digits + "_-@.+")

    for i, c in enumerate(emailStr):
        if c not in acceptableChars:
            return False
        if i == 0 and c == "@":
            return False
        if i == 0 and c == ".":
            return False
        if c == "." and emailStr[i-1] in "@.":
            return False
        if hasa == True and c == "@":
            return False
        if i == len(emailStr)-1 and c == ".":
            return False
        if c == "@":
            hasa=True
        if hasa == True  and c == ".":
            hasp = True

    if hasa and hasp:
        return True
    
    return False

def usernameSanitation(inputStr:str):
    acceptableChars = set(string.ascii_lowercase + string.ascii_uppercase + string.digits + "_" + "-" )
    for c in inputStr:
        if c not in acceptableChars:
            return False
    return True

def pwStrengthChecker(password:str):

    if 8 > len(password) <= 128:
        # print("too long, too short")
        return False
    
    if password.islower():
        # print("no uppercase")
        return False
    
    if password.isupper():
        # print("no lowercase")
        return False
    
    if password.isdigit():
        # print("onlynumber")
        return False
    
    specialCharacters = "!@#$%^&*()_-=+[]|:;<>?/\".,\\"
    numbers = "0123456789"
    hasSpecChar=False
    hasNumber=False
    for char in password:

        if hasSpecChar == False and char in specialCharacters:
            hasSpecChar = True
    
        if hasNumber == False and char in numbers:
            hasNumber = True

    if not hasSpecChar:
        # print("no spec char")
        return False
    if not hasNumber:
        # print("no number")
        return False

    return True

def saltDecoder(encodedSalt):
    return base64.b64decode(encodedSalt)

def saltEncoder(decodedSalt):
    return base64.b64encode(decodedSalt).decode("utf-8")
    
def salter(rawPassword:str)->bytes:
    salt = urandom(64)
    binaryPassword = rawPassword.encode("utf-8")
    saltedPassword = binaryPassword + salt
    encodedSalt = saltEncoder(salt)
    salt = saltDecoder(encodedSalt)
    return encodedSalt, saltedPassword

def hasher(saltedPassword:bytes)->str:
    hash = ph.hash(saltedPassword)
    return hash

def pwVerifier(previousHash, rawpassword, encodedSalt):

    binaryPassword = rawpassword.encode("utf-8")
    salt = saltDecoder(encodedSalt)
    saltedPassword = binaryPassword + salt
    return ph.verify(previousHash, saltedPassword)

def main():
    pass

if __name__ == "__main__":
    main()