#!/usr/bin/python3

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v0')

from api.v0.views.achievements import *
from api.v0.views.games import *
from api.v0.views.news import *
from api.v0.views.pieces import *
from api.v0.views.users import *
from api.v0.views.users_friends import *
from api.v0.views.users_achievements import *
