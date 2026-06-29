from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from mail import sendEmail

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
csrf = CSRFProtect(app)

app_password = os.getenv("app_password")


class SubscriptionForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    email = StringField("Электронная почта", validators=[DataRequired()])
    submit = SubmitField("Отправить")


@app.route("/", methods=["GET", "POST"])
def index(name=None):
    form = SubscriptionForm()
    return render_template("index.html", form=form)


@csrf.exempt
@app.route("/api/subscribe", methods=["POST"])
def subscription_post():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400

    name = data.get("name")
    email = data.get("email")

    sendEmail(app_password, name, email)
    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    app.run(debug=True)
