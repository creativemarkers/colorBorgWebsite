from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from security import salter, hasher, saltDecoder, pwVerifier

app = Flask(__name__)
app.secret_key = "Ce5w9nw4aAfK9XXKVpwhP4rFh5nft9bf3h4vGYLpUnwANtvADucBMpJpejdreFdXptGAbbDz4xdrAA7SSqn33NB5gkNbKBQRgU5VwLZkxqVLUPRdA2M5bMQY7vERgXFdHFAPpzwZrtzkLks99UUqqQCcDf6uh42M"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    salt = db.Column(db.String(128))
    hash = db.Column(db.String(200))
    email = db.Column(db.String(200))


    def __init__(self,name,salt,hash,email):
        self.name = name
        self.salt = salt
        self.hash = hash
        self.email = email

@app.route("/")
def home():
    return render_template("index0.html")

@app.route("/view")
def view():
    return render_template("view.html", values = Users.query.all())

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        pw = request.form["pw"]
        session["user"] = user

        foundUser = Users.query.filter_by(name=user).first()
    
        if foundUser:
            encodedsalt = foundUser.salt
            print(type(encodedsalt))
            hash = foundUser.hash
            pwVerifier(hash,pw,encodedsalt)
            # if not pwVerifier(hash,pw,salt):
            #     flash("Wrong Password,try again")
            #     return render_template("login0.html")

            session["email"] = foundUser.email

        else:
            salt, saltedPassword = salter(pw)
            hash = hasher(saltedPassword)
            # retry =  salt + pw.encode("utf-8")
            usr = Users(user, salt, hash, None)
            db.session.add(usr)
            db.session.commit()

        flash("Login Succesful!")
        return redirect(url_for("download"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("download"))
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
    
@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}","info")
        session.pop("user", None)
        session.pop("email",None)
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