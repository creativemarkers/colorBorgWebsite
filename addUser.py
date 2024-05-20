from colorBorgFlask import app, db, Users
from security import salter, hasher

"""
unlock user
"""


def addUser(username,password,role, email=None,company=None,jobTitle=None):
    with app.app_context():
        username =  username
        password = password
        role = role

        foundUser = Users.query.filter_by(name=username).first()
        if foundUser:
            print("foundUser")
            return False

        salt, saltedPassword = salter(password)
        hash = hasher(saltedPassword)
        # retry =  salt + pw.encode("utf-8")
        usr = Users(username, salt, hash, role, email, company, jobTitle)
        db.session.add(usr)
        db.session.commit()

        print(f"Added, {username}")
        return True
if __name__ == "__main__":
    addUser("testUser", "1", "user", "bilboBaggingsJr@theshire.com")