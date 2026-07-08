from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, csrf
import os


def get_password():
    return os.getenv("app_password")


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shaurmania.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from app import models  # noqa

        db.create_all()

        from app import routes  # noqa

    return app
