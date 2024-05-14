from flask import Flask
from markupsafe import escape
from flask import url_for, redirect
from flask import request
from flask import render_template

from markupsafe import Markup

app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'index'

# @app.route('/login')
# def login():
#     return 'login'

# @app.route('/user/<username>')
# def profile(username):
#     return f'{username}\'s profile'

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login',next='/'))
#     print(url_for('profile', username='Fern beCAriNE'))

# @app.route('/login',methods=['GET','POST'])
# def login():
#     if request.method == 'POST'"
#         return do_the_login()
#     else:
#         return show_the_login_form()
    
# @app.get('/login')
# def login_get():
#     return show_the_login_form()

# @app.post('/login')
# def login_post():
#     return do_the_login()



# from flask import render_template

# @app.route('/hello')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html',name=name)


#how to load your own html and css files
#add html to the a folder called templates
#and your css and js scripts into a folder called static
#then use the following lines of code to render them
@app.route('/')
def home():
    url_for('static', filename='styles.css')
    return render_template('index.html')

@app.route("/user/<name>/")
def username(name):
    return render_template("hello.html",content="Testing")

@app.route("/test")
def tester():
    return render_template("new.html",content="Testing")


# @app.route("/<name>")
# def user(name):
#     return f"Hello, {name}"

# @app.route("/admin/")
# def admin():
#     return redirect(url_for("user", name="admin!"))



