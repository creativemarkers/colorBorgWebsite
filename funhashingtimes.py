from os import urandom
from argon2 import PasswordHasher

ph = PasswordHasher()

pw = input("what would you like to hash?:")
pwBytes = pw.encode("utf-8")
print(pwBytes)
salt = urandom(64)
print(salt)

saltedpw = pwBytes+salt

hash = ph.hash(saltedpw)

print(len(hash))
print(type(hash))