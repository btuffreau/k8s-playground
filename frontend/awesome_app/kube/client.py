import logging
from typing import List, Dict, Any

from kubernetes import client, config


class K8s:
    def __init__(self) -> None:
        try:
            config.incluster_config.load_incluster_config()
        except config.config_exception.ConfigException:
            try:
                config.kube_config.load_kube_config(context="kind-aetion")
                logging.warning("Using kube local config")
            except config.config_exception.ConfigException:
                raise RuntimeError("Cannot initialise kubernetes clients.")
        self.client = client.CoreV1Api()

    def list_pods(self) -> list[dict[str, str | Any]]:
        try:
            response = self.client.list_namespaced_pod(namespace="aetion").items
        except client.exceptions.ApiException as e:
            logging.error(e.body)
            raise RuntimeError(e.body)
        output = [{"podName": podinfo.metadata.name,
                   "creationTime": str(podinfo.metadata.creation_timestamp), }
                  for podinfo in response if podinfo.metadata]
        return output


if __name__ == "__main__":

    try:
        raise RuntimeError("Cannot initialise kubernetes clients.")
    except RuntimeError as e:
        print(type(e).__name__)
