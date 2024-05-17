import base64
from os import urandom
from argon2 import PasswordHasher

ph = PasswordHasher()




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
    print(type(encodedSalt))
    salt = saltDecoder(encodedSalt)
    print(type(salt))
    

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
    salter("caca")
    pass

if __name__ == "__main__":
    main()