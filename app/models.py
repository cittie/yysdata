import json
from . import db
from config import basedir
from flask import url_for

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
    LIGHTING = 8

class BattleCounter(db.Model):
    __tablename__ = 'battle_counters'
    id = db.Column(db.Integer, primary_key=True, index=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('missions.id'), index=True)
    shikigami_id = db.Column(db.Integer, db.ForeignKey('shikigamis.id'), index=True)    # Which monster is used
    stamina_cost = db.Column(db.Integer)
    amount = db.Column(db.Integer)      # How many monsters in this counter
    group_leader = db.Column(db.Boolean, default=False)     # Only for
    order = db.Column(db.Integer)       # Appears on which round, max 3

class ShikiSoulSet(db.Model):
    __tablename__ = 'shiki_soul_sets'
    id = db.Column(db.Integer, primary_key=True, index=True)
    soul_id = db.Column(db.Integer, db.ForeignKey('souls.id'), index=True)
    shikigami_id = db.Column(db.Integer, db.ForeignKey('shikigamis.id'), index=True)

class Shikigami(db.Model):
    __tablename__ = 'shikigamis'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(128), unique=True, index=True)
    rarity = db.Column(db.String(4))
    role = db.Column(db.String(16))
    awaken_materials = db.Column(db.String(16))
    battle_counters = db.relationship('BattleCounter', backref='shikigami', lazy='joined')
    shiki_soul_sets = db.relationship('ShikiSoulSet', backref='shikigami', lazy='joined')

    def __repr__(self):
        return '<%r>' % self.name

class Mission(db.Model):
    __tablename__ = 'missions'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(128), index=True)
    mission_type = db.Column(db.Integer)
    mission_stamina_cost = db.Column(db.Integer)
    soul_id = db.Column(db.Integer, db.ForeignKey('souls.id'))
    battle_counters = db.relationship('BattleCounter', backref='mission', lazy='joined')

    def to_json(self):
        json_mission = {
            'url': url_for('api.get_mission', id=self.id, _external=True),
            'name': self.name,
            'battle_counters': url_for('api.get_battle_counters', id=self.id, _external=True)
        }
        return json_mission

    @staticmethod
    def get_shikigamis_in_mission(mission):
        shikigamis = db.session.query(Shikigami).join(BattleCounter).filter(
            BattleCounter.mission_id == mission.id
        )
        return shikigamis

    @staticmethod
    def get_shiki_name_amount_pair(mission, shikigamis):
        name_amount_pair = []
        for shiki in shikigamis:
            shiki_count = 0
            for battle_counter in mission.battle_counters:
                if battle_counter.shikigami_id == shiki.id:
                    shiki_count += battle_counter.amount
            name_amount_pair.append((shiki.name, shiki_count))
        return name_amount_pair

    @staticmethod
    def get_missions_with_shikigami(shikigami):
        missions = db.session.query(Mission).join(BattleCounter).filter(
            BattleCounter.shikigami_id == shikigami.id)
        return missions

    @staticmethod
    def get_mission_name_shikigami_amount_pair(missions, shikigami):
        '''
        :param
         mission: obj
         shikigami: obj
        :return: list of tuples: [(mission.name, shikigami.amount), ...]
        '''
        name_amount_pair = []
        for mission in missions:
            shiki_count = 0
            for battle_counter in mission.battle_counters:
                if battle_counter.shikigami_id == shikigami.id:
                    shiki_count += battle_counter.amount
            name_amount_pair.append((mission.name, shiki_count))
        name_amount_pair.sort(key=lambda x: x[1], reverse=True)
        return name_amount_pair

class AssistantSoul(db.Model):
    __tablename__ = 'souls'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    position = db.Column(db.Integer)
    drop_missions = db.relationship('Mission', backref='soul', lazy='joined')
    attr_2_pieces = db.Column(db.String(64))
    attr_4_pieces = db.Column(db.String(256))
    shiki_soul_sets = db.relationship('ShikiSoulSet', backref='soul', lazy='joined')


def init_data():
    import_shikigami_data()
    import_mission_data()

def load_from_json(table_name):
    with open(basedir + "/data/" + table_name + ".json") as json_file:
        data = json.load(json_file)
    return data

def import_shikigami_data():
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

def import_mission_data():
    Mission.query.delete()
    BattleCounter.query.delete()
    data = load_from_json(Mission.__tablename__)
    for d in data:
        mission = Mission(name=d['name'])

        counters = d['counters']
        stamina_cost = d['stamina_cost']
        mission_stamina_cost = 0

        for i, counter in enumerate(counters):
            for monster, amount in counter.items():
                shikigami = Shikigami.query.filter_by(name=monster).first()
                battle_counter = BattleCounter(
                    mission=mission,
                    shikigami=shikigami,
                    stamina_cost=stamina_cost,
                    amount=amount,
                    order=i+1
                )
                mission_stamina_cost += stamina_cost
                db.session.add(battle_counter)

        mission.mission_stamina_cost = mission_stamina_cost
        db.session.add(mission)
    db.session.commit()

