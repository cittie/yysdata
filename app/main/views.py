# -*- coding: utf-8 -*-

import collections
from . import main
from .. import db
from flask import render_template, redirect, url_for, flash, current_app, request
from ..models import Shikigami, Mission, BattleCounter
from forms import MissionQueryForm, RewardQuestQueryForm


@main.route('/')
def index():
    shikigamis = Shikigami.query.order_by(Shikigami.rarity.desc())
    return render_template('index.html', shikigamis=shikigamis)


@main.route('/mission_query', methods=['GET', 'POST'])
def mission_query():
    form = MissionQueryForm()
    if form.validate_on_submit():
        shikigamis = Mission.get_shikigamis_in_mission(form.mission.data)
        mission_info = Mission.get_shiki_name_amount_pair(form.mission.data, shikigamis)
        return render_template('mission_query_result.html',
                               mission=form.mission.data,
                               mission_info=mission_info)
    return render_template('mission_query.html', form=form)




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
        mission_dict = collections.defaultdict(int)
        for shiki in shikis_group:
            missions = Mission.get_missions_with_shikigami(shiki)
            if missions:
                for mission in missions:
                    mission_dict[mission] += 1
                name_count_pairs = Mission.get_mission_name_shikigami_amount_pair(missions, shiki)
                mission_data.append((shiki, name_count_pairs))
        common_missions = [(mission.name, count) for mission, count in mission_dict.items() if count > 1]
        common_missions.sort(key=lambda x: x[1], reverse=True)
        return render_template('reward_quest_query_result.html',
                               common_missions=common_missions,
                               mission_data=mission_data
                               )

    return render_template('reward_quest_query.html', form=form)
