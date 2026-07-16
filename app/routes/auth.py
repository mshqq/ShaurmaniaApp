from flask_login import login_user, logout_user, login_required
from flask import Blueprint, jsonify, request
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Запрос не содержит JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Не указан логин или пароль"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Неверный логин или пароль"}), 401

    login_user(user)
    return jsonify({"message": "Успешный вход"}), 200


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Вы вышли"}), 200
