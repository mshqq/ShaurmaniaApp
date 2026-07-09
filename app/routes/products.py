from flask import Blueprint, jsonify
from app.models import Product
from app.extensions import csrf

products_bp = Blueprint("products", __name__)


@csrf.exempt
@products_bp.route("/api/products", methods=["GET"])
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
