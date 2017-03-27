import unittest
from flask import current_app
from app import create_app, db
from app.models import Shikigami, Mission, BattleCounter

class ShikigamiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_shikigami_creating(self):
        shikigami = Shikigami(
            name='Test Shikigami',
            rarity='N'
        )

        self.assertIsNotNone(shikigami)
        self.assertEqual(shikigami.name, 'Test Shikigami')
        self.assertEqual(shikigami.rarity, 'N')
