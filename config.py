import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://dkmztdztlmebao:4cb43db4738fb7d03ca189130d255faa3140679fa011798598168df40952c344@ec2-107-21-255-181.compute-1.amazonaws.com:5432/d1s1adhbe6m35q')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')