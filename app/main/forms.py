# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import Shikigami, Mission, BattleCounter


def all_shikigamis():
    return Shikigami.query

class RewardQuestQueryForm(FlaskForm):
    shikigami1 = QuerySelectField(u'式神1', query_factory=all_shikigamis, get_label='name', validators=[DataRequired()])
    shikigami2 = QuerySelectField(u'式神2', query_factory=all_shikigamis, get_label='name')
    shikigami3 = QuerySelectField(u'式神3', query_factory=all_shikigamis, get_label='name')
    shikigami4 = QuerySelectField(u'式神3', query_factory=all_shikigamis, get_label='name')
    submit = SubmitField(u'提交')