from . import main
from flask import render_template, redirect, url_for, flash, current_app, request
from ..models import Shikigami, Mission

@main.route('/')
def index():
    shikigamis = Shikigami.query.order_by(Shikigami.rarity.desc())
    return render_template('index.html', shikigamis=shikigamis)

@main.route('/missions')
def show_missions():
    missions = Mission.query.order_by(Mission.name)
    return render_template('missions.html', missions=missions)