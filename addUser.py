from colorBorgFlask import app, db, Users
from security import salter, hasher


def changePassword(username, newpassword):
    with app.app_context():
        foundUser = Users.query.filter_by(name=username).first()
        if foundUser:
            salt, saltedPassword = salter(newpassword)
            hash = hasher(saltedPassword)
            foundUser.salt = salt
            foundUser.hash = hash
            db.session.commit()

            print(f"{username}'s password has been changed")
        else:
            print("user not found")

def changeRole(username,role):
    with app.app_context():
        foundUser = Users.query.filter_by(name=username).first()
        if foundUser:
            oldRole = foundUser.role
            foundUser.role = role
            db.session.commit()
            print(f"changed {username} role from: {oldRole}, to {role}")

def unlockUser(username):
    with app.app_context():
        foundUser = Users.query.filter_by(name=username).first()
        if foundUser:
            print(foundUser.lockedOut, foundUser.loginAttempts)
            foundUser.lockedOut = False
            foundUser.loginAttempts = 0
            db.session.commit()
            print(f"{username} has been unlocked")
        else:
            print("user not found")

def addUser(username,password,role, email=None,company=None,jobTitle=None):
    with app.app_context():
        username =  username
        password = password
        role = role

        foundUser = Users.query.filter_by(name=username).first()
        if foundUser:
            print("user already exsits")
            return False

        salt, saltedPassword = salter(password)
        hash = hasher(saltedPassword)

        usr = Users(username, salt, hash, role, email, company, jobTitle)
        db.session.add(usr)
        db.session.commit()

        print(f"Added, {username}")
        return True
    
if __name__ == "__main__":
    pass
    
   