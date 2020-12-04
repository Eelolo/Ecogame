import os

from dotenv import load_dotenv

# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '.env'))

FLASK_APP = os.getenv('FLASK_APP')
ENV = os.getenv('FLASK_ENV')
RUN_PORT = os.getenv('FLASK_RUN_PORT')
DEBUG = os.getenv('FLASK_DEBUG')




