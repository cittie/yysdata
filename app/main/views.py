# -*- coding: utf-8 -*-

import collections
from . import main
from .. import db
from flask import render_template, redirect, url_for, flash, current_app, request, abort
from flask_sqlalchemy import get_debug_queries
from ..models import Shikigami, Mission, BattleCounter
from forms import MissionQueryForm, RewardQuestQueryForm, ShikigamiQueryForm


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['YYSDATA_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning('show query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' %
                                       (query.statment, query.parameters, query.duration, query.context))
    return response

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/shikigami_query', methods=['GET', 'POST'])
def shikigami_query():
    form = ShikigamiQueryForm()
    if form.validate_on_submit():
        shikigami = form.shikigami.data
        return render_template('shikigami_query_result.html',
                               shikigami=shikigami
                               )
    return render_template('mission_query.html', form=form)

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
        common_missions.sort(key=lambda x: x[0])
        common_missions.sort(key=lambda x: x[1], reverse=True)
        return render_template('reward_quest_query_result.html',
                               common_missions=common_missions,
                               mission_data=mission_data
                               )

    return render_template('reward_quest_query.html', form=form)

@main.route('/shutdown')
def server_shutdown():
    if not current_app.test:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'