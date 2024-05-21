import os
from datetime import timedelta

class Config:
    #will need to add the secret key to the getenv
    SECRET_KEY = "Ce5w9nw4aAfK9XXKVpwhP4rFh5nft9bf3h4vGYLpUnwANtvADucBMpJpejdreFdXptGAbbDz4xdrAA7SSqn33NB5gkNbKBQRgU5VwLZkxqVLUPRdA2M5bMQY7vERgXFdHFAPpzwZrtzkLks99UUqqQCcDf6uh42M"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Users.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    TEMPLATES_AUTO_RELOAD = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
    RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')