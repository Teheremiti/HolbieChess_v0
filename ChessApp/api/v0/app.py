#!usr/bin/python3
""" API routes and endpoints for the Flask app """

from models import storage
from api.v0.views import app_views
from os import environ
from flask import Flask, render_template, make_response, jsonify

app = Flask(__name__)
app.config['JSONIFY_PretTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
