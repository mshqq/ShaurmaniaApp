from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request, current_app, render_template
from flask_login import login_required
from app.extensions import db, csrf
from app.utils import to_local_time
from app.models import Order, OrderItems, Location, Product
from apscheduler.schedulers.background import BackgroundScheduler
from re import compile

orders_bp = Blueprint("orders", __name__)
scheduler = BackgroundScheduler()

STATUS_DELAYS = [("cooking", 10), ("pending", 15), ("done", 20)]
PHONE_REGEX = compile(r"^7\d{10}$")


def setStatus(app, id, status):
    with app.app_context():
        order = Order.query.filter(Order.id == id).first()
        if order is None:
            app.logger.info(f"Заказ с ID={id} не найден, статус {status} не установлен")
            return
        try:
            app.logger.info(
                f"Заказ с ID={id} - старый статус: {order.status} - Новый статус: {status}"
            )
            order.status = status
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)


@csrf.exempt
@orders_bp.route("/api/order/status/<string:token>", methods=["GET"])
def get_order_status(token):
    order = Order.query.filter(Order.public_token == token).first()
    if not order:
        return jsonify({"error": "Не найден заказ"}), 404
    status = order.status

    return jsonify({"status": status}), 200


@csrf.exempt
@orders_bp.route("/api/order/<string:token>", methods=["GET"])
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
@orders_bp.route("/order/<string:token>", methods=["GET"])
def render_order(token):
    order = (
        Order.query.options(
            joinedload(Order.locations),
            joinedload(Order.items).joinedload(OrderItems.product),
        )
        .filter(Order.public_token == token)
        .first()
    )
    if order is None:
        return render_template("404.html")

    if order.delivery_type == "Доставка":
        dType = "Курьером"
    else:
        dType = order.delivery_type

    if order.locations:
        address = order.locations.address
    else:
        address = order.delivery_address

    order_items = [
        {
            "product_id": item.product_id,
            "name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
        }
        for item in order.items
    ]

    return render_template(
        "order.html",
        oId=order.id,
        cName=order.customer_name,
        cPhone=order.customer_phone,
        dType=dType,
        address=address,
        orderItems=order_items,
        total=order.total_price,
        status=order.status,
        created_at=to_local_time(order.created_at, fmt="%H:%M", minutes=2),
    )


@orders_bp.route("/api/order", methods=["POST"])
def make_order():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Некорректный JSON"}), 400

    name = data.get("customer_name")
    phone = data.get("customer_phone")
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

    if not PHONE_REGEX.match(phone):
        return jsonify({"error": "Некорректный формат номера телефона!"}), 400

    if delivery_type not in ("Самовывоз", "Доставка"):
        return jsonify({"error": "Некорректный тип доставки!"}), 400

    if not cart:
        return jsonify({"error": "Корзина пуста!"}), 400

    products_map = {}

    for item in cart:
        product_id = item.get("id")
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
            product_id = item.get("id")
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

        try:
            start_time = datetime.now()
            app = current_app._get_current_object()
            for status, delay_seconds in STATUS_DELAYS:
                scheduler.add_job(
                    setStatus,
                    trigger="date",
                    run_date=start_time + timedelta(seconds=delay_seconds),
                    args=[app, new_order.id, status],
                    id=f"order-{new_order.id}-{status}",
                    replace_existing=True,
                )
        except Exception:
            current_app.logger.exception(
                "Не удалось запланировать статусы заказа %s", new_order.id
            )

        return jsonify(
            {
                "message": "Заказ был создан",
                "redirect_url": f"/order/{new_order.public_token}",
            }
        ), 201

    except Exception as e:
        current_app.logger.exception(e, exc_info=True)
        db.session.rollback()
        return jsonify({"error": "Ошибка создания заказа!"}), 500


@csrf.exempt
@orders_bp.route("/api/orders", methods=["GET"])
@login_required
def get_orders():
    orders = Order.query.options(
        joinedload(Order.locations),
        joinedload(Order.items).joinedload(OrderItems.product),
    ).all()
    orders_list = []
    for order in orders:
        composition_list = [
            {
                "name": item.product.name,
                "quantity": item.quantity,
                "subtotal": item.product.price * item.quantity,
            }
            for item in order.items
        ]

        info = {
            "order_id": order.id,
            "customer_name": order.customer_name,
            "customer_phone": order.customer_phone,
            "status": order.status,
            "total_price": order.total_price,
            "created_at": to_local_time(order.created_at),
        }

        if order.delivery_type == "Самовывоз":
            info["delivery_type"] = "Самовывоз"
            info["location"] = order.locations.address if order.locations else None

        if order.delivery_type == "Доставка":
            info["delivery_type"] = "Доставка"
            info["delivery_address"] = order.delivery_address

        info["composition"] = composition_list

        orders_list.append(info)

    return jsonify(orders_list), 200
