from time import sleep

from flask import Blueprint, make_response, Response

healthz_blueprint = Blueprint('healthz', __name__, )

EXECUTION_TIME = 3


@healthz_blueprint.route('/healthz')
def healthz() -> Response:
    sleep(EXECUTION_TIME)
    payload = {"status": "ok", "execution_seconds": EXECUTION_TIME, "service": "frontend"}
    return make_response(payload)
