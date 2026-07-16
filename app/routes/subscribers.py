from flask_login import login_required
from flask import Blueprint, jsonify, request
from app.models import Subscriber
from app.extensions import db, csrf
from re import compile
from datetime import datetime
from sqlalchemy.exc import IntegrityError
# from mail import sendEmail
# from app import get_password

subscribers_bp = Blueprint("subscribers", __name__)
EMAIL_REGEX = compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@csrf.exempt
@subscribers_bp.route("/unsubscribe/<string:token>")
def unsubscribe(token):
    sub = Subscriber.query.filter(Subscriber.unsubscribe_token == token).first()

    if not sub:
        return jsonify({"error": "Токен не найден или устарел!"}), 404

    if sub.is_active is False:
        return jsonify({"error": "Вы уже отписались от рассылки!"}), 400

    try:
        sub.is_active = False
        db.session.commit()
        return jsonify({"message": "Вы успешно отписались от рассылки!"})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Произошла ошибка при отписке!"}), 500


@subscribers_bp.route("/admin/subscribers")
@login_required
def view_subscribers():
    subs = Subscriber.query.filter(Subscriber.is_active == True).all()  # noqa
    sub_list = [
        {
            "name": sub.name,
            "email": sub.email,
            "unsubscribe_token": sub.unsubscribe_token,
            "subscribed_at": sub.subscribed_at,
            "is_active": sub.is_active,
        }
        for sub in subs
    ]
    print(sub_list)

    if not sub_list:
        return jsonify({"message": "Нет подписчиков!"}), 200

    return jsonify(sub_list)


@csrf.exempt
@subscribers_bp.route("/api/subscribe", methods=["POST"])
def subscription_post():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Запрос не содержит JSON"}), 400

    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "Не указано имя!"}), 400

    email = (data.get("email") or "").strip()
    if not email:
        return jsonify({"error": "Не указана почта!"}), 400

    if not EMAIL_REGEX.match(email):
        return jsonify({"error": "Некорректный формат почты!"}), 400

    existing = Subscriber.query.filter(Subscriber.email == email).first()
    if existing:
        if existing.is_active:
            return jsonify({"error": "Электронная почта уже подписана!"}), 400
        else:
            existing.is_active = True
            existing.subscribed_at = datetime.utcnow()
            db.session.commit()
            return jsonify({"message": "Вы снова подписаны!"}), 200

    try:
        new_sub = Subscriber(name=name, email=email)  # pyrefly: ignore
        db.session.add(new_sub)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Электронная почта уже подписана!"}), 400

    # app_password = get_password()
    # sendEmail(app_password, name, email)
    return jsonify({"message": "Успешно"}), 200
