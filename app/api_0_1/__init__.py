from flask import Blueprint

api = Blueprint('api', __name__)

from . import shikigamis, missions, battle_counters, errors
