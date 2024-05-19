import os
from datetime import timedelta

class Config:
    SECRET_KEY = "Ce5w9nw4aAfK9XXKVpwhP4rFh5nft9bf3h4vGYLpUnwANtvADucBMpJpejdreFdXptGAbbDz4xdrAA7SSqn33NB5gkNbKBQRgU5VwLZkxqVLUPRdA2M5bMQY7vERgXFdHFAPpzwZrtzkLks99UUqqQCcDf6uh42M"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Users.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
    TEMPLATES_AUTO_RELOAD = True
