from flask import Flask
from infrastructure.entrypoint.controllers.bancolombia_controller import bancolombia
from infrastructure.database.connection import db
from infrastructure.database.config import Config

app_aux = Flask(__name__)
app_aux.register_blueprint(bancolombia)

# def create_app():
#     app_aux = Flask(__name__)
#     app_aux.config.from_object(Config)
#
#     db.init_app(app_aux)
#     app_aux.register_blueprint(bancolombia)
#
#     return app_aux
#
#
# def setup_database(app_aux):
#     with app_aux.app_context():
#         db.create_all()
#
#
# app = create_app()
# setup_database(app)
