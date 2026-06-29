from http.server import HTTPServer
from storage import Storage


class Path:
    REGISTER = "/register"
    LOGIN = "/login"
    LOGOUT = "/logout"

    @staticmethod
    def get_paths():
        return [Path.REGISTER, Path.LOGIN, Path.LOGOUT]


class Server(HTTPServer):
    def __init__(self, address, request_handler, paths: Path, db: Storage):
        super().__init__(address, request_handler)
        self.path = paths
        self.db = db
        print(f"Server initialized with paths: {paths.get_paths()}")