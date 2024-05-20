from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from security import salter, hasher, saltDecoder, pwVerifier, pwStrengthChecker, usernameSanitation
from admin import admin
from argon2.exceptions import VerifyMismatchError

app = Flask(__name__)
app.register_blueprint(admin, url_prefix="")

app.config.from_object('config.Config')

db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    salt = db.Column(db.String(128),nullable=False)
    hash = db.Column(db.String(200),nullable=False)
    role = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(200),nullable=True)
    company = db.Column(db.String(200),nullable=True)
    jobTitle = db.Column(db.String(200),nullable=True)
    loginAttempts = db.Column(db.Integer,nullable=False,default=0)

    def __init__(self,name,salt,hash,role,email=None,company=None,jobTitle=None):
        self.name = name
        self.salt = salt
        self.hash = hash
        self.role = role
        self.email = email
        self.company = company
        self.jobTitle = jobTitle

@app.route("/")
def home():
    return render_template("index0.html")

@app.route("/login", methods=["POST","GET"])
def login():

    if "user" in session:
        flash("Already Logged In!")
        return redirect(url_for("download"))
    
    if request.method == "POST":
        
        if request.form["login"]:
                # return render_template("login0.html")
            user = request.form["nm"]
            if not usernameSanitation(user):
                flash("usernames may only include lowercase, uppercase letters,digits, _ and - ")
                return render_template("login0.html")
            pw = request.form["pw"]
            foundUser = Users.query.filter_by(name=user).first()
        
            if foundUser:
                encodedsalt = foundUser.salt

                hash = foundUser.hash
                try:
                    pwVerifier(hash,pw,encodedsalt)
                except VerifyMismatchError:
                    #need to add a logging and lockout here
                    flash("You've entered the wrong password or Username! Try Again")
                    return render_template("login0.html")
                session.permanent = True
                session["user"] = user
                session["role"] = foundUser.role
                session["email"] = foundUser.email
    
                flash("Login Succesful!")
                return redirect(url_for("download"))
            else:
                flash("You've entered the wrong password or Username! Try Again")
                return render_template("login0.html")

    return render_template("login0.html")


@app.route("/download", methods=["POST","GET"])
def download():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email=request.form["email"]
            session["email"] = email
            foundUser = Users.query.filter_by(name=user).first()
            foundUser.email = email
            db.session.commit()
            flash("Your Email has been saved!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("download0.html", user=user, email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))
    

@app.route("/userAccountCreation", methods=["POST", "GET"])
def userAccountCreation():

    if "user" in session:
        flash("Already Logged In!")
        return redirect(url_for("download"))
    
    if request.method == "POST":

        username = request.form["usn"]
        if not usernameSanitation(username):
            flash("usernames may only include lowercase, uppercase letters,digits, _ and - ")
            return render_template("login0.html")
        password = request.form["pw"]
        password2 = request.form["pw2"]
        email = request.form["email"]

        foundUser = Users.query.filter_by(name=username).first()

        if foundUser:
            flash("Account with that username already exsists")
            return render_template("createAccount.html")
        
        if password != password2:
            flash("passwords do not match")
            return render_template("createAccount.html")
        
        if pwStrengthChecker(password):
            from addUser import addUser
            addUser(username,password,"user",email)
            flash("Account created Successfully")

            return redirect(url_for("login"))
        else:
            flash("Password must be longer than 8 characters, make sure to include upper and lower case letters, a number, and at least one special charcter!")
            return render_template("createAccount.html")


    return render_template("createAccount.html")


@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}","info")
        session.pop("user", None)
        session.pop("email",None)
        session.pop("role",None)
        return redirect(url_for("login"))
    else:
        flash(f"You're not logged in")
        return redirect(url_for("login"))
    
def main():
    app.run(debug=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    main()