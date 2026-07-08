from app.extensions import db
from datetime import datetime
from uuid import uuid4


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    address = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Locations {self.id}>"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    public_token = db.Column(db.String(250), unique=True, default=lambda: str(uuid4()))

    customer_name = db.Column(db.String(150), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)

    delivery_type = db.Column(db.String(20), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=True)
    delivery_address = db.Column(db.String(255), nullable=True)

    status = db.Column(db.String(50), default="Новый")
    total_price = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    locations = db.relationship("Location")
    items = db.relationship("OrderItems", backref="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order {self.id}>"


class OrderItems(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    product = db.relationship("Product")

    def __repr__(self):
        return f"<OrderItems {self.id}>"


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text)
    composition = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f"<Products {self.name}>"


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    slug = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)

    products = db.relationship("Product", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class Subscriber(db.Model):
    __tablename__ = "subscribers"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    unsubscribe_token = db.Column(
        db.String(250), default=lambda: str(uuid4()), unique=True
    )
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Subscribers {self.email}>"
