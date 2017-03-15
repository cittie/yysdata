from . import db

class Rarity:
    SSR = 1
    SR = 2
    R = 3
    N = 4

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


class Shikigami(db.Model):
    __tablename__ = 'shikigamis'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    rarity = db.Column(db.Integer)
    reward_quests = db.relationship('RewardQuest', backref='shikigami', lazy='dynamic')

class Mission(db.Model):
    __tablename__ = 'missions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    mission_type = db.Column(db.Integer)
    stamina_cost = db.Column(db.Integer)
    soul_id = db.Column(db.Integer, db.ForeignKey('soul.id'))

class Assistant_Soul(db.Model):
    __tablename__ = 'souls'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    drop_missions = db.relationship('Mission', backref='soul', lazy='joined')

class RewardQuest(db.Model):
    __tablename__ = 'reward_quests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text())
    shikigami_id = db.Column(db.Integer, db.ForeignKey('shikigami.id'))