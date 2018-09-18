import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'lines.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
ERROR_404_HELP = False