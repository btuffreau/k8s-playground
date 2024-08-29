import logging

from flask import Flask

from .services.healthz import healthz_blueprint
from .services.index import index_blueprint
from .services.kubeinfo import kubeinfo_blueprint

from .config.config import ApplicationConfig

app = Flask(__name__)

app.config.from_object(ApplicationConfig())

logging.info(app.config)

app.register_blueprint(index_blueprint)
app.register_blueprint(healthz_blueprint)
app.register_blueprint(kubeinfo_blueprint)
