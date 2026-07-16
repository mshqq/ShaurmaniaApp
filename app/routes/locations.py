from flask import Blueprint, jsonify, request
from flask_login import current_user
from app.extensions import db, csrf
from app.models import Location
from sqlalchemy.exc import IntegrityError

locations_bp = Blueprint("locations", __name__)


@csrf.exempt
@locations_bp.route("/api/locations", methods=["GET", "POST"])
def create_location():
    if request.method == "GET":
        locations = Location.query.all()
        location_list = [{"id": item.id, "address": item.address} for item in locations]
        return jsonify(location_list), 200

    if not current_user.is_authenticated:
        return jsonify({"error": "Требуется авторизация"}), 401

    data = request.get_json()

    if not data:
        return jsonify({"error": "Запрос не содержит JSON!"}), 400

    address = data.get("address")
    if not address:
        return jsonify({"error": "Не передан адрес новой точки!"}), 400

    try:
        new_location = Location(address=address)  # pyrefly: ignore
        db.session.add(new_location)
        db.session.commit()
        return jsonify({"message": "Успешно создано"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Уже существует точка с таким адресом!"}), 400
