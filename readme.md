# to do
    ~hash passwords~
    ~~create an account request page~~
    ~~admin portal for me to easily create accounts~~
    ~~easily delete users~~ or change their permissions
    add my socials and more then likely make my github repo public
    password reset
    add analytics, hits, from where, if it came a from a  user, what links what they pressed 

    pretty up the stuff i made on the backend

# low hanging security fruit 

You're welcome! Here are a few more low-hanging fruit security measures for your Flask application:

1. Enable Secure Headers
Use Flask extensions like flask-talisman to add secure headers to your responses.

python
Copy code
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app)
2. SQLAlchemy ORM Usage
Avoid raw SQL queries to prevent SQL injection. Use SQLAlchemy ORM methods.

python
Copy code
# Safe query using ORM
user = User.query.filter_by(username='example_user').first()
3. Handle User Authentication and Authorization
Use libraries like Flask-Login for user authentication and Flask-Principal for authorization.

python
Copy code
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
4. Rate Limiting
Prevent abuse by rate limiting requests using Flask-Limiter.

python
Copy code
from flask_limiter import Limiter

limiter = Limiter(app)
5. Error Handling
Customize error pages to avoid exposing sensitive information.

python
Copy code
@app.errorhandler(404)
def page_not_found(e):
    return "Page not found!", 404
Implementing these measures will improve your Flask app's security without requiring extensive changes.