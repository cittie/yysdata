import unittest
from flask import url_for
from app import create_app, db
import app.models as md
from app.models import Mission, Shikigami

class YysdataClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        md.init_data()

        self.client = self.app.test_client(use_cookies=True)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue(response.status_code, 200)

    def test_mission_query_page(self):
        response = self.client.get(url_for('main.mission_query'))
        self.assertTrue(response.status_code, 200)

    def test_quest_query_page(self):
        response = self.client.get(url_for('main.quest_query'))
        self.assertTrue(response.status_code, 200)

        shiki1 = Shikigami.query.get(64)
        shiki2 = Shikigami.query.get(32)

        response = self.client.post(url_for('main.quest_query'), data = {
            'shikigami1': shiki1,
            'shikigami2': shiki2
        })
        self.assertTrue(response.status_code, 302)