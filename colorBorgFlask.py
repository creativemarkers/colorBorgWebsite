from flask import Flask, render_template, request, session, redirect, url_for, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "Ce5w9nw4aAfK9XXKVpwhP4rFh5nft9bf3h4vGYLpUnwANtvADucBMpJpejdreFdXptGAbbDz4xdrAA7SSqn33NB5gkNbKBQRgU5VwLZkxqVLUPRdA2M5bMQY7vERgXFdHFAPpzwZrtzkLks99UUqqQCcDf6uh42M"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    return render_template("index0.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        pw = request.form["pw"]
        session["user"] = user

        flash("Login Succesful!")
        return redirect(url_for("download"))
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("download"))
        return render_template("login0.html")

@app.route("/download")
def download():
    if "user" in session:
        user = session["user"]
        return render_template("download0.html", user=user)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}","info")
        session.pop("user", None)
        return redirect(url_for("login"))
    else:
        flash(f"You're not logged in")
        return redirect(url_for("login"))
    
def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()