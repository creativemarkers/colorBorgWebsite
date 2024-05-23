from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from security import salter, hasher, saltDecoder, pwVerifier, pwStrengthChecker, usernameSanitation, emailValidator
from argon2.exceptions import VerifyMismatchError
from extensions import limiter
from flask_wtf import CSRFProtect
from flask_mail import Mail, Message
from flask_talisman import Talisman
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)

csp = {
    'default-src': [
        '\'self\'',
        'cdnjs.cloudflare.com',
        'stackpath.bootstrapcdn.com',
        'fonts.googleapis.com',  # Allow Google Fonts
        'fonts.gstatic.com'      # Allow Google Fonts
    ],
    'style-src': [
        '\'self\'',
        'cdnjs.cloudflare.com',
        'stackpath.bootstrapcdn.com',
        'fonts.googleapis.com',
        '\'unsafe-inline\''
    ],
    'font-src': [
        '\'self\'',
        'fonts.googleapis.com',
        'fonts.gstatic.com'
    ],
    'script-src': [
        '\'self\'',
        'cdnjs.cloudflare.com',
        'stackpath.bootstrapcdn.com',
    ],
    'img-src': [
        '\'self\'',
        'data:'
    ]
}

app.config.from_object('config.Config')

limiter.init_app(app=app)
csrf = CSRFProtect(app)
csrf.init_app(app)
mail = Mail(app)
Talisman(app, content_security_policy=csp)

from admin import admin

app.register_blueprint(admin, url_prefix="")

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
    lockedOut = db.Column(db.Boolean,nullable=False,default=False)

    def __init__(self,name,salt,hash,role,email=None,company=None,jobTitle=None):
        self.name = name
        self.salt = salt
        self.hash = hash
        self.role = role
        self.email = email
        self.company = company
        self.jobTitle = jobTitle
        self.loginAttempts = 0
        self.lockedOut = False

@app.route("/")
def home():
    return render_template("index0.html")

@app.route("/login", methods=["POST","GET"])
@limiter.limit("1/second",override_defaults=False)
def login():

    if "user" in session:
        flash("Already Logged In!")
        return redirect(url_for("download"))
    
    if request.method == "POST":
        
        if request.form["login"]:

            user = request.form["nm"]
            if not usernameSanitation(user):
                flash("usernames may only include lowercase, uppercase letters,digits, _ and - ")
                return render_template("login0.html")
            pw = request.form["pw"]
            foundUser = Users.query.filter_by(name=user).first()
        
            if foundUser:
                if foundUser.lockedOut == True:
                    flash("Account locked out, please contact the site admin.")
                    return render_template("login0.html")
                
                encodedsalt = foundUser.salt
                hash = foundUser.hash

                try:
                    pwVerifier(hash,pw,encodedsalt)
                except VerifyMismatchError:
                    #need to add a logging and lockout here
                    flash("You've entered the wrong password or Username! Try Again")
                    foundUser.loginAttempts += 1
                    db.session.commit()
                    print(foundUser.loginAttempts)
                    if foundUser.loginAttempts >= 4:
                        flash("You have one more attempt before you're locked out")
                    if foundUser.loginAttempts >= 5:
                        foundUser.lockedOut = True
                        db.session.commit()
                    return render_template("login0.html")
                
                foundUser.loginAttempts = 0
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
    if "user" not in session:
        flash("You are not logged in!")
        return redirect(url_for("login"))
    
    user = session["user"]
    email = session["email"]
    return render_template("download0.html", user=user, email=email)

@app.route('/download/<filename>')
def downloadFile(filename):

    if "user" not in session:
        flash("You need to be logged in to download this file")
        return redirect(url_for('login'))
    
    if "downloads" not in session:
        session["downloads"] = 1

    if session["downloads"] <= 5:

        session["downloads"] += 1
        with open('logs/downloads.txt', 'rb') as downloadLog:
            downloadLog.seek(-2, os.SEEK_END)
            while downloadLog.read(1) != b'\n':
                downloadLog.seek(-2, os.SEEK_CUR)
            lastLine = downloadLog.readline().decode()

            lastDlNumber =  None
            for i,c, in enumerate(lastLine):
                if c == " ":
                    lastDlNumber = lastLine[:i]
                    lastDlNumber =  int(lastDlNumber)
                    break
        with open('logs/downloads.txt', 'a', encoding="utf-8") as downloadLog:
            downloadLog.write(f"{lastDlNumber+1} {session['user']} {filename} {datetime.now()} \n")

        return send_from_directory(directory='static/files', path=filename)
    else:
        flash("Too many downloads today")
        return redirect(url_for('download'))

@app.route("/userAccountCreation", methods=["POST", "GET"])
@limiter.limit("1/second",override_defaults=False)
def userAccountCreation():

    if "user" in session:
        flash("Already Logged In!")
        return redirect(url_for("download"))
    
    if request.method == "POST":

        username = request.form["usn"]
        if not usernameSanitation(username):
            flash("usernames may only include lowercase, uppercase letters,digits, _ and - ")
            return render_template("createAccount.html")
        password = request.form["pw"]
        password2 = request.form["pw2"]
        email = request.form["email"]
        if not emailValidator(email):
            flash("INVALID EMAIL")
            return render_template("createAccount.html")

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
    
@app.route("/contactMe", methods=["POST","GET"])
def contactMe():

    if "user" not in session:
        flash("Please log in to get in touch with me!")
        return redirect('login')

    if "contactMeCount" not in session:
        session['contactMeCount'] = 0

    if request.method == "POST":
        # with limiter.limit
        if session["contactMeCount"] <= 2:
            msgContent = request.form['message']
            recip = app.config['RECIPIENT_EMAIL']
            try:
                msg = Message(f"Message from ContactMe | {app.name}", body=f"FROM:{session['user']}, EMAIL:{session['email']}, CONTENT: {msgContent}",
                            recipients=[recip]
                )
                mail.send(msg)
                flash("Message sent")
            except Exception as e:
                flash(e)
        else:
            flash("You've contacted me too many times in 24hours")
    return render_template("contactMe.html")

@app.errorhandler(404)
def pageNotFound(e):
    return render_template('404.html'),404

@app.route('/trigger-error')
def trigger_error():
    raise Exception("This is a test exception to trigger a 500 error")

@app.errorhandler(500)
def internalServerError(e):
    return render_template("500.html"),500

def main():
    app.run(debug=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    main()