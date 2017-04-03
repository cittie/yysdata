import unittest
import threading
from app import create_app, db, models
from selenium import webdriver

class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.client = webdriver.Chrome()
        except:
            pass

        if cls.client:
            cls.app = create_app('test')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            db.create_all()
            models.init_data()

            threading.Thread(target=cls.app.run).start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            db.drop_all()
            db.session.remove()

            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass
    