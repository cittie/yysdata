from . import main
from flask import render_template, redirect, url_for, flash, current_app, request
from ..models import Shikigami, Mission
from forms import RewardQuestQueryForm


@main.route('/')
def index():
    shikigamis = Shikigami.query.order_by(Shikigami.rarity.desc())
    return render_template('index.html', shikigamis=shikigamis)


@main.route('/missions')
def show_missions():
    missions = Mission.query.order_by(Mission.name)
    return render_template('missions.html', missions=missions)


@main.route('/reward_quest_query', methods=['GET', 'POST'])
def quest_query():
    form = RewardQuestQueryForm()
    #amounts = range(1, 16)
    #form.amount1 = form.amount2 = amounts
    if form.validate_on_submit():
        missions1 = Mission.query.filter(Mission.shikigamis.contains(form.shikigami1.data))
        return render_template('reward_quest_query_result.html', missions=missions1)
    return render_template('reward_quest_query.html', form=form)
