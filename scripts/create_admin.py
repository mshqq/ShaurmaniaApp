import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from getpass import getpass
from app import create_app
from app.extensions import db
from app.models import User
from sys import exit


def create_admin():
    app = create_app()
    with app.app_context():
        username = input("Юзернейм: ").strip()
        email = input("Email: ").strip()
        password = getpass("Пароль: ").strip()

        if not username or not email or not password:
            exit("Все поля обязательны")

        if User.query.filter_by(username=username).first():
            exit(f"Пользователь {username} уже существует")

        if User.query.filter_by(email=email).first():
            exit(f"Email {email} уже занят")

        user = User(username=username, email=email)  # pyrefly: ignore
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        print(f"Создан пользователь {username} (id={user.id})")


if __name__ == "__main__":
    create_admin()
