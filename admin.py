from flask import Blueprint, render_template, session, flash, redirect, url_for, request

admin = Blueprint("admin",__name__, static_folder="static", template_folder="templates")

@admin.route("/admin_panel/")
@admin.route("/admin/")
def adminPanel():
    role =  session.get("role")
    print(role)
    if not "user" in session:
        flash("Not logged in.")
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        flash("Insufficient Permissions")
        return redirect(url_for("download"))
    return render_template("adminPanel.html")

@admin.route("/admin_panel/create_user", methods=["POST","GET"])
def createAccountPanel():
    from addUser import addUser
    if not "user" in session:
        flash("Not logged in.")
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        flash("Insufficient Permissions")
        return redirect(url_for("download"))
    
    if request.method == "POST":
        user = request.form["nm"]
        password = request.form["pw"]
        role = request.form["role"]

        if not addUser(user,password,role):
            flash("Error: User Exists")
        else:
            flash("User Added Successfully")
    return render_template("adminCreateAccount.html")

@admin.route("/admin_panel/view")
def view():
    #could possibly include a dropdown to edit users, and even create from there, and a delete button
    from colorBorgFlask import app, Users
    if not "user" in session:
        flash("Not logged in.")
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        flash("Insufficient Permissions")
        return redirect(url_for("download"))
    with app.app_context():
        values = Users.query.all()
        return render_template("view.html", values = values)

@admin.route("/admin_panel/deleteUsers", methods=['POST', 'GET'])
def deleteUsers():
    if not "user" in session:
        flash("Not logged in.")
        return redirect(url_for("login"))
    if session.get("role") != "admin":
        flash("Insufficient Permissions")
        return redirect(url_for("download"))

    if request.method == 'POST':

        from colorBorgFlask import app, Users

        if request.form["test"]:
            # print("test2")
            username = request.form["nm"]
            # print(type(username))
            with app.app_context():
                foundUser = Users.query.filter_by(name=username).first()
                if foundUser:
                    if foundUser.name == session["user"]:
                        flash("You can't delete the account your logged into!")
                        return render_template("deleteUser.html")
                    else:
                        return render_template("deleteUser.html", value = foundUser) 
                else:
                    flash("User not found!")
                    return render_template("deleteUser.html")
                
        if request.form["test2"]:
            from colorBorgFlask import db
            username = request.form["test2"]
            print(username)
            with app.app_context():
                foundUser = Users.query.filter_by(name=username).first()
                db.session.delete(foundUser)
                db.session.commit()
                flash(f"{username} has been deleted")
    return render_template("deleteUser.html")


