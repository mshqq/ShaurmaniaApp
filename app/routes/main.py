from flask import Blueprint, render_template
from flask_login import login_required
from app.forms import SubscriptionForm


main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index(name=None):
    form = SubscriptionForm()
    return render_template("index.html", form=form)


@main_bp.route("/debug", methods=["GET"])
@login_required
def debug():
    return render_template("base.html")
