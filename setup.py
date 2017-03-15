from setuptools import setup, find_packages

setup(name='yysdata',
      version='0.1',
      description='Quickly search for yys data',
      author='Yee Joen',
      author_email='yi.jiang.gameloft@gmail.com',

      install_requires=[
          'flask-script',
          'flask-bootstrap',
          'flask-wtf',
          'flask-sqlalchemy',
          'flask-migrate'
      ]
      )