# to do
    make my github colorborg repo public?
    need to provide a link for the actual bot
    add email icon at footer, make it do something

    more security

        flask talisman

        1. Enable Secure Headers
        Use Flask extensions like flask-talisman to add secure headers to your responses.

        python
        Copy code
        from flask import Flask
        from flask_talisman import Talisman

        app = Flask(__name__)
        Talisman(app)

        ~~email sanitation~~
        ~~account lockouts~~
        ~~rate limiting~~

    what do you want to log
        rate limits being exceeded and by whom, if it's a user id like to know
        account creations
        account logins, account logouts
        account lockouts
        admin account attempts
        errors caused 
        when social links or contact links clicked

    fix about section
    logging
    need to add the below column
    # company = db.Column(db.String(200))
    # jobTitle = db.Column(db.String(200))
    add analytics, hits, from where, if it came a from a  user, what links what they pressed 
    password reset
    change user permissions
    pretty up the stuff i made on the backend