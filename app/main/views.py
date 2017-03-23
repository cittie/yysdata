from . import main
from .. import db
from flask import render_template, redirect, url_for, flash, current_app, request
from ..models import Shikigami, Mission, BattleCounter
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
    if form.validate_on_submit():
        missions1 = db.session.query(Mission).join(BattleCounter).filter(
            BattleCounter.shikigami_id == form.shikigami1.data.id)
        missions2 = db.session.query(Mission).join(BattleCounter).filter(
            BattleCounter.shikigami_id == form.shikigami2.data.id)
        missions3 = db.session.query(Mission).join(BattleCounter).filter(
            BattleCounter.shikigami_id == form.shikigami2.data.id)
        return render_template('reward_quest_query_result.html',
                               missions1=missions1,
                               missions2=missions2,
                               missions3=missions3)
    return render_template('reward_quest_query.html', form=form)
