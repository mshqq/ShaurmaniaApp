from flask import current_app as app, render_template, request, jsonify
from app.models import Subscriber, Product, Order, OrderItems, Location
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
@app.route("/api/locations", methods=["POST"])
def create_location():
    data = request.get_json()

    address = data.get("address")
    new_location = Location(address=address)  # pyrefly: ignore
    db.session.add(new_location)
    db.session.commit()

    return jsonify({"message": "Успешно создано"}), 200


@csrf.exempt
@app.route("/order/<string:token>", methods=["GET"])
def get_order_info(token):
    order = Order.query.filter(Order.public_token == token).first_or_404()

    order_list = [
        {"product": item.product.name, "qty": item.quantity} for item in order.items
    ]
    order_json = {
        "id": order.id,
        "customer_name": order.customer_name,
        "customer_phone": order.customer_phone,
        "order_items": order_list,
    }
    return jsonify(order_json), 200


@csrf.exempt
@app.route("/api/order", methods=["POST"])
def make_order():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Некорректный JSON"}), 400

    name = data.get("name")
    phone = data.get("phone")
    delivery_type = data.get("delivery_type")
    location_id = data.get("location_id")
    delivery_address = data.get("delivery_address")

    if delivery_type == "Доставка":
        location_id = None
        if not delivery_address:
            return jsonify({"error": "Не указан адрес доставки"}), 400

    if delivery_type == "Самовывоз":
        delivery_address = None
        if not location_id:
            return jsonify({"error": "Не указана точка самовывоза"}), 400

        if not Location.query.filter(Location.id == location_id).first():
            return jsonify({"error": "Указана несуществующая точка самовывоза"}), 400

    cart = data.get("cart")

    if not name:
        return jsonify({"error": "Не введено имя заказчика!"}), 400

    if not phone:
        return jsonify({"error": "Не введен номер телефона!"}), 400

    if delivery_type not in ("Самовывоз", "Доставка"):
        return jsonify({"error": "Некорректный тип доставки!"}), 400

    if not cart:
        return jsonify({"error": "Корзина пуста!"}), 400

    products_map = {}

    for item in cart:
        product_id = item.get("product_id")
        quantity = item.get("quantity")

        if not product_id:
            return jsonify({"error": "У товара нет product_id"}), 400

        product = Product.query.filter(Product.id == product_id).first()

        if not product:
            return jsonify({"error": "Указан несуществующий товар!"}), 400

        if quantity is None:
            return jsonify({"error": "У товара нет quantity"}), 400

        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({"error": "quantity должно быть числом больше 0"}), 400

        products_map[product_id] = product

    try:
        total = 0
        new_order = Order(
            customer_name=name,  # pyrefly: ignore
            customer_phone=phone,  # pyrefly: ignore
            delivery_type=delivery_type,  # pyrefly: ignore
            location_id=location_id,  # pyrefly: ignore
            delivery_address=delivery_address,  # pyrefly: ignore
        )
        db.session.add(new_order)
        db.session.flush()

        for item in cart:
            product_id = item.get("product_id")
            quantity = item.get("quantity")

            product = products_map[product_id]

            total += product.price * quantity
            new_item = OrderItems(
                order_id=new_order.id,  # pyrefly: ignore
                product_id=product_id,  # pyrefly: ignore
                quantity=quantity,  # pyrefly: ignore
            )
            db.session.add(new_item)

        new_order.total_price = total
        db.session.commit()

        return jsonify({"message": "Заказ был создан", "order_id": new_order.id}), 201

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": "Ошибка создания заказа!"}), 500


@csrf.exempt
@app.route("/api/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    orders_list = [
        {
            "id": order.id,
            "public_token": order.public_token,
            "customer_name": order.customer_name,
            "customer_phone": order.customer_phone,
            "delivery_type": order.delivery_type,
            "location_id": order.location_id,
            "delivery_address": order.delivery_address,
            "status": order.status,
            "total_price": order.total_price,
            "created_at": order.created_at,
        }
        for order in orders
    ]

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
