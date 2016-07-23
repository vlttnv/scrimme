from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_openid import OpenID
from flask_login import LoginManager

scrimme = Flask(__name__)
scrimme.config.from_object('config')
db = SQLAlchemy(scrimme)
oid = OpenID(scrimme)
lm = LoginManager(scrimme)

from scrimme import views, models