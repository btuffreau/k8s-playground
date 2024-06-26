from http import HTTPStatus
from flask import Blueprint, make_response, Response
from awesome_app.kube.client import K8s

kubeinfo_blueprint = Blueprint('kubeinfo', __name__, )

kubernetes_client = K8s()


@kubeinfo_blueprint.route('/kube/info')
def info() -> Response:
    try:
        data = kubernetes_client.list_pods()
    except RuntimeError as e:
        return make_response({"service": "frontend", "error": f"oops, {type(e).__name__} occurred", "status": "error"},
                             HTTPStatus.SERVICE_UNAVAILABLE
                             )
    return make_response(data, HTTPStatus.OK)
