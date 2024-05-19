import base64
from os import urandom
from argon2 import PasswordHasher

ph = PasswordHasher()

def pwStrengthChecker(password:str):

    if 8 > len(password) <= 128:
        return False
    
    if password.islower():
        return False
    
    if password.isupper():
        return False
    
    if password.isdigit():
        return False
    
    specialCharacters = "!@#$%^&*()_-=+[]|:;<>/., "
    numbers = "0123456789"
    hasSpecChar=False
    hasNumber=False
    for char in password:

        if hasSpecChar == False and char in specialCharacters:
            hasSpecChar = True
    
        if hasNumber == False and char in numbers:
            hasNumber = True

    if not hasSpecChar:
        return False
    if not hasNumber:
        return False

    return True

def saltDecoder(encodedSalt):
    return base64.b64decode(encodedSalt)
    pass

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
    # salter("caca")
    result = pwStrengthChecker("cacaPeePoo!1")
    print(result)
    result = pwStrengthChecker("cacaP!10")
    print(result)
    pass

if __name__ == "__main__":
    main()