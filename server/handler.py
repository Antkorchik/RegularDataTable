from http.server import BaseHTTPRequestHandler
from json import dumps, loads
import hashlib


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f'GET request to: {self.path}')

        if self.path == "/":
            response = dumps({'message': "Server is running!"})
            self.set_response(response)

        elif self.path.startswith("/users/"):  # ← ДОБАВЬТЕ ЭТО
            login = self.path[7:]  # "/users/test" → "test"
            user = self.server.db.get_user(login)

            if user:
                response = dumps({
                    "login": user.login,
                    "id": user.user_id,
                    "created": user.created_at.isoformat()
                })
                self.set_response(response)
            else:
                response = dumps({"error": "User not found"})
                self.set_response(response, 404)

        else:
            self.handle_404()

    def do_POST(self):
        print(f"POST request to: {self.path}")
        try:
            if self.path == self.server.path.REGISTER:
                self.register_impl()
            elif self.path == self.server.path.LOGIN:
                self.login_impl()
            elif self.path == self.server.path.LOGOUT:
                self.logout_impl()
            else:
                self.handle_404()
        except Exception as e:
            print(f"Error in POST routing: {e}")
            error_response = dumps({"error": "Internal server error"})
            self.set_response(error_response, 500)

    def handle_404(self):
        error_response = dumps({
            "message": f"Route {self.path} does not exist"
        })
        self.set_response(error_response, 404)

    def set_response(self, response, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def register_impl(self):
        try:
            data = self.get_post_body()
            login = data.get("login")
            password = data.get("password")
            if not login or not password:
                error_response = dumps({"message": "Login and password are required!"})
                self.set_response(error_response, 400)
                return

            user = self.server.db.register_user(login=login, password=password)
            if user is None:
                error_response = dumps({"message": "User already exists!"})
                self.set_response(error_response, 400)
            else:
                response = dumps({
                    "message": "User registered successfully!",
                    "user_id": user.user_id,
                    "login": user.login
                })
                self.set_response(response, 201)
        except Exception as e:
            print(f"Error in register_impl: {e}")
            error_response = dumps({"message": "Internal server error"})
            self.set_response(error_response, 500)

    def get_post_body(self):
        content_len = int(self.headers.get('Content-Length', 0))
        if content_len == 0:
            return {}
        post_body = self.rfile.read(content_len)
        return loads(post_body.decode('utf-8'))

    def login_impl(self):
        try:
            data = self.get_post_body()
            login = data.get("login")
            password = data.get("password")
            if not login or not password:
                error_response = dumps({"message": "Login and password are required!"})
                self.set_response(error_response, 400)
                return

            user = self.server.db.get_user(login)
            if user is None:
                error_response = dumps({"message": "User not found!"})
                self.set_response(error_response, 404)
                return

            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user.password != hashed_password:
                error_response = dumps({"message": "Invalid password!"})
                self.set_response(error_response, 401)
                return

            self.server.db.update_last_active(login)
            response = dumps({
                "message": "Login successful!",
                "user_id": user.user_id,
                "login": user.login,
                "last_active_at": user.last_active_at.isoformat()
            })
            self.set_response(response)
        except Exception as e:
            print(f"Error in login_impl: {e}")
            error_response = dumps({"message": "Internal server error"})
            self.set_response(error_response, 500)

    def logout_impl(self):
        response = dumps({"message": "Logout successful!"})
        self.set_response(response)

    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {format % args}")