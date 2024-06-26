import os


class ApplicationConfig(object):

    @property
    def BACKEND_URL(self) -> str:
        return os.environ.get("BACKEND_URL", "http://backend.default.cluster.local:8000")
