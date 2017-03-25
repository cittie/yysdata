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
    '''
    mission_data structure:
    [shiki<obj>, [(mission name<str>, shiki amount<int>), ...]
    '''
    form = RewardQuestQueryForm()
    if form.validate_on_submit():
        shikis_group = (form.shikigami1.data, form.shikigami2.data, form.shikigami3.data, form.shikigami4.data)
        mission_data = []
        for shiki in shikis_group:
            missions = Mission.get_missions_with_shikigami(shiki)
            if missions:
                name_count_pairs = Mission.get_name_shikigami_amount(missions, shiki)
                mission_data.append((shiki, name_count_pairs))
        return render_template('reward_quest_query_result.html', mission_data=mission_data)

    return render_template('reward_quest_query.html', form=form)
