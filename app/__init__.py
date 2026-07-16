from flask import Flask
from dotenv import load_dotenv
from app.extensions import db, csrf
from app.routes.locations import locations_bp
from app.routes.main import main_bp
from app.routes.orders import orders_bp
from app.routes.products import products_bp
from app.routes.subscribers import subscribers_bp
from os import getenv


def get_password():
    return getenv("app_password")


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shaurmania.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.sort_keys = False

    db.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from app import models  # noqa

        db.create_all()

        from app import routes  # noqa

    app.register_blueprint(locations_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(subscribers_bp)

    from app.routes.orders import scheduler

    if not scheduler.running:
        scheduler.start()

    return app
