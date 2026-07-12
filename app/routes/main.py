from flask import Blueprint, render_template
from app.forms import SubscriptionForm


main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index(name=None):
    form = SubscriptionForm()
    return render_template("index.html", form=form)


@main_bp.route("/debug", methods=["GET"])
def debug():
    return render_template("base.html")
