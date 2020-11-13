import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'app/static/rot/')
    UPLOADS_DEFAULT_URL = 'http://localhost:5000/static/rot/'
    UPLOADED_IMAGES_DEST = os.path.join(basedir, 'app/static/rot/')
    UPLOADED_IMAGES_URL = 'http://localhost:5000/static/rot/'
    DISPLAY_PER_PAGE = 10
    ADMINS = ['robbyhp@yahoo.co.id', 'teguh2pra@gmail.com']