from flask import Flask
from infrastructure.entrypoint.controllers.bancolombia_controller import bancolombia

app_aux = Flask(__name__)
app_aux.register_blueprint(bancolombia)

