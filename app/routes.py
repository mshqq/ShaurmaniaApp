from flask import current_app as app, render_template, request, jsonify
from app.models import Subscriber, Product, Order, OrderItems
from app.extensions import db, csrf
from app.forms import SubscriptionForm
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import re
# from mail import sendEmail
# from app import get_password

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


@app.route("/", methods=["GET", "POST"])
def index(name=None):
    form = SubscriptionForm()
    return render_template("index.html", form=form)


@csrf.exempt
@app.route("/api/order", methods=["POST"])
def make_order():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400

    summaryPrice = 0
    name = data.get("name")
    phone = data.get("phone")
    cart = data.get("cart")

    print("\nНовый заказ\n")
    print(f"Имя: {name}")
    print(f"Телефон: {phone}")
    print("\nСостав заказа:\n")

    for c in cart:
        summaryPrice += c["qty"] * c["price"]
        print(f"{c['name']} - {c['qty']} шт.")

    print(f"\nСумма заказа: {summaryPrice} ₽\n")

    response_data = {
        "status": "success",
        "message": f"Заказ для {name} успешно принят!",
    }

    return jsonify(response_data), 200


@csrf.exempt
@app.route("/api/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    orders_list = [{"id": o.id} for o in orders]

    order_items = OrderItems.query.all()
    order_items_list = [{"id": oi} for oi in order_items]
    return jsonify(orders_list, order_items_list), 200


@csrf.exempt
@app.route("/api/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    product_list = [
        {
            "id": p.id,
            "category": p.category.slug,
            "name": p.name,
            "slug": p.slug,
            "description": p.description,
            "composition": p.composition,
            "price": p.price,
            "image_path": p.image_path,
        }
        for p in products
    ]
    print(product_list)

    return jsonify(product_list), 200


@csrf.exempt
@app.route("/api/subscribe", methods=["POST"])
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


@app.route("/admin/subscribers")
def view_subscribers():
    subs = Subscriber.query.filter(Subscriber.is_active is True).all()
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


@app.route("/unsubscribe/<string:token>")
def unsubscribe(token):
    sub = Subscriber.query.filter(Subscriber.unsubscribe_token == token).first()

    if sub.is_active is False:
        return jsonify({"error": "Вы уже отписались от рассылки!"}), 400

    if not sub:
        return jsonify({"error": "Токен не найден или устарел!"}), 404

    try:
        sub.is_active = False
        db.session.commit()
        return jsonify({"message": "Вы успешно отписались от рассылки!"})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Произошла ошибка при отписке!"}), 500
