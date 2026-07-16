from app import create_app
from dotenv import load_dotenv
from os import getenv
from sys import exit

load_dotenv()

app = create_app()

if __name__ == "__main__":
    debug = getenv("FLASK_DEBUG", "0") == "1"
    host = getenv("FLASK_HOST", "127.0.0.1")
    port = int(getenv("FLASK_PORT", 5000))

    if not (1 <= port <= 65535):
        exit(f"FLASK_PORT={port} вне диапазона 1-65535")

    app.run(
        debug=debug,
        host=host,
        port=port,
    )
