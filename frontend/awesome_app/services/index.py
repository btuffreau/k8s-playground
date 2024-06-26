from http import HTTPStatus

import requests
from flask import Blueprint, Response, make_response, current_app

index_blueprint = Blueprint('index', __name__, )


@index_blueprint.route('/')
def index() -> Response:
    backend_url: str = str(current_app.config.get("BACKEND_URL"))
    try:
        response = requests.get(backend_url, timeout=1)
        response.raise_for_status()
        backend_data = response.json()['message']
    except requests.exceptions.RequestException:
        return process_backend_response(f"{backend_url} is not reachable", HTTPStatus.SERVICE_UNAVAILABLE)

    return process_backend_response(f"{backend_data} from the other side", HTTPStatus.OK)


def process_backend_response(msg: str, code: HTTPStatus) -> Response:
    status = "ok" if code == HTTPStatus.OK else "error"
    payload = {'service': "frontend", "status": status, "message": msg}
    return make_response(payload, code)
