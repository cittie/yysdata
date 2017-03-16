import json
from . import db
from config import basedir

def load_from_json(table_name):
    with open(basedir + "\\data\\" + table_name + ".json") as json_file:
        data = json.load(json_file)
    return data

class MissionType:
    STORY = 1
    SOUL_DUNGEON = 2
    AWAKE_DUNGEON = 3
    MONSTERS_SEALING = 4
    MONSTER_NIAN = 5
    STONE_DISTANCE = 6
    GOLD_MONSTER = 7
    EXP_MOSNTER = 8
    SECTOR_BREAKING = 9

class AwakenMaterialValue:
    FIRE = 1,
    WIND = 2,
    WATER = 4,
    LIGHT = 8

class BattleCounter(db.Model):
    __tablename__ = 'battle_counters'
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('missions.id'), index=True)
    shikigami_id = db.Column(db.Integer, db.ForeignKey('shikigamis.id'), index=True)
    group_leader = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer)

class Shikigami(db.Model):
    __tablename__ = 'shikigamis'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    rarity = db.Column(db.String(4))
    awaken_materials = db.Column(db.String(16))
    missions = db.relationship('Mission', secondary='battle_counters',
                                 backref=db.backref('mission', lazy='joined'),
                                 lazy='dynamic')

    @staticmethod
    def import_data():
        Shikigami.query.delete()
        data = load_from_json(Shikigami.__tablename__)
        for d in data:
            shiki = Shikigami(
                name=d['name'],
                rarity = d['rarity'],
                awaken_materials = d['awaken_materials']
            )
            db.session.add(shiki)
        db.session.commit()

class Mission(db.Model):
    __tablename__ = 'missions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    mission_type = db.Column(db.Integer)
    stamina_cost = db.Column(db.Integer)
    soul_id = db.Column(db.Integer, db.ForeignKey('souls.id'))
    shikigamis = db.relationship('Shikigami', secondary='battle_counters',
                                 backref=db.backref('shikigami', lazy='joined'),
                                 lazy='dynamic')

class Assistant_Soul(db.Model):
    __tablename__ = 'souls'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    position = db.Column(db.Integer)
    drop_missions = db.relationship('Mission', backref='soul', lazy='joined')
    attr_2_pieces = db.Column(db.String(64))
    attr_4_pieces = db.Column(db.String(256))

class RewardQuest(db.Model):
    __tablename__ = 'reward_quests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text())
    shikigami_id = db.Column(db.Integer, db.ForeignKey('shikigamis.id'))
    amount = db.Column(db.Integer)


