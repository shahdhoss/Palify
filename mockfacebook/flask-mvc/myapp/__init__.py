from flask import Flask
from .controllers import errors
from .controllers import main
from .controllers.main import loginmanager_init
from .models.User import db
from sqlalchemy import inspect
# import extensions
# import config

blueprints = (main, errors)
DB_NAME = "MainDB.db"
def create_app():
   app = Flask(__name__, template_folder='../templates')
   app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
   app.secret_key='ana_esmy_shahd'
   loginmanager_init(app)
   db.init_app(app)
   with app.app_context():
      inspector = inspect(db.engine)
      if not inspector.has_table('user'):
         create_database(app)
   # app.config.from_object(config.ConfigObject)
   init_blueprints(app)
   init_extensions(app)
   init_other(app)
   return app

def init_blueprints(app):
   for bp in blueprints:
      app.register_blueprint(bp)

def init_extensions(app):
   pass

def init_other(app):
   pass
def create_database(app):
    with app.app_context():
        db.create_all()
        print('DB created successfully')
