import argparse
from server import Server, Path
from handler import Handler
from storage import Storage

def start_server(addr, port, server_class=Server, handler_class=Handler):
    try:
        server_address = (addr, port)
        print(f"Starting server on {addr}:{port}")
        paths = Path()
        storage = Storage()
        http_server = server_class(server_address, handler_class, paths, storage)
        print("Server started successfully!")
        print("Available endpoints:")
        for path in paths.get_paths():
            print(f"  http://{addr}:{port}{path}")
        http_server.serve_forever()
    except Exception as e:
        print(f"Failed to start server: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Сервер авторизации",
        usage="Используйте параметры --listen, port чтобы задать URL", )
    parser.add_argument(
        "-l",
        "--listen",
        default="127.0.0.1",
        help="IP адрес сервера", )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Порт", )
    args = parser.parse_args()
    start_server(addr=args.listen, port=args.port)