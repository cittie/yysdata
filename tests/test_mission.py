import unittest
from flask import current_app
from app import create_app, db, models
from app.models import Shikigami, Mission, BattleCounter


class MissionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_mission_creating(self):
        mission = Mission(
            name='Test Mission',
            mission_type=0,
            mission_stamina_cost=6
        )

        self.assertIsNotNone(mission.name)
        self.assertIsNotNone(mission.mission_type)
        self.assertIsNotNone(mission.mission_stamina_cost)

    def test_battle_counter_creating(self):
        mission = Mission(
            name='Test Mission',
            mission_type=0,
            mission_stamina_cost=30
        )

        shikigami = Shikigami(
            name='Test Shikigami',
            rarity='N'
        )

        battle_counter = BattleCounter(
            mission=mission,
            shikigami=shikigami,
            stamina_cost=6,
            amount=11,
            order=1
        )

        self.assertTrue(battle_counter in mission.battle_counters)
        self.assertTrue(battle_counter in shikigami.battle_counters)
        self.assertEqual(battle_counter.stamina_cost, 6)

class MissionDataTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_data_is_clear_before_init(self):
        self.assertEqual(Shikigami.query.count(), 0)
        self.assertEqual(Mission.query.count(), 0)

    def test_init_data(self):
        models.init_data()
        self.assertTrue(Shikigami.query.count() > 0)
        self.assertTrue(Mission.query.count() > 0)