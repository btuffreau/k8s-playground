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

# TODO prepare role/role binding for service account with wrong permissions :)
# TODO add helm to the ec2 instance, so the user can do something with it: install some release, create one from scratch
