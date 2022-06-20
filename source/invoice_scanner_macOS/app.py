#!/usr/bin/env python3

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail
from db_setup import init_db, db_session
from flask import Flask, render_template
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "dNQYWs@T%q$pu#y@yYc!AEw-LXW65_@T"
db = SQLAlchemy(app)
mail = Mail()
