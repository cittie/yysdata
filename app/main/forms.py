# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Shikigami, Mission, BattleCounter


def all_shikigamis():
    return Shikigami.query

def all_missions():
    return Mission.query

class ShikigamiQueryForm(FlaskForm):
    shikigami = QuerySelectField(u'式神', query_factory=all_shikigamis, get_label='name',
                               validators=[DataRequired()])
    submit = SubmitField(u'提交')

class RewardQuestQueryForm(FlaskForm):
    shikigami1 = QuerySelectField(u'式神1', query_factory=all_shikigamis, get_label='name',
                                  validators=[DataRequired()])
    shikigami2 = QuerySelectField(u'式神2', query_factory=all_shikigamis, get_label='name')
    shikigami3 = QuerySelectField(u'式神3', query_factory=all_shikigamis, get_label='name')
    shikigami4 = QuerySelectField(u'式神4', query_factory=all_shikigamis, get_label='name')
    submit = SubmitField(u'提交')

class MissionQueryForm(FlaskForm):
    mission = QuerySelectField(u'关卡', query_factory=all_missions, get_label='name',
                               validators=[DataRequired()])
    submit = SubmitField(u'提交')