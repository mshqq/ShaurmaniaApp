from flask import Blueprint, jsonify, request
from app.extensions import db, csrf
from app.utils import to_local_time
from app.models import Order, OrderItems, Location, Product

orders_bp = Blueprint("orders", __name__)


@csrf.exempt
@orders_bp.route("/order/<string:token>", methods=["GET"])
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
@orders_bp.route("/api/order", methods=["POST"])
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
@orders_bp.route("/api/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    orders_list = []
    for order in orders:
        composition = OrderItems.query.filter(OrderItems.order_id == order.id).all()
        composition_list = []

        for item in composition:
            product = Product.query.filter(Product.id == item.product_id).first()
            composition_list.append(
                {
                    "name": product.name,
                    "quantity": item.quantity,
                    "subtotal": product.price * item.quantity,
                }
            )

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
            info["location"] = (
                Location.query.filter(Location.id == order.location_id).first().address
            )

        if order.delivery_type == "Доставка":
            info["delivery_type"] = "Доставка"
            info["delivery_address"] = order.delivery_address

        info["composition"] = composition_list

        orders_list.append(info)

    return jsonify(orders_list), 200
