from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from mail import sendEmail

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app_password = os.getenv("app_password")


class SubscriptionForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    email = StringField("Электронная почта", validators=[DataRequired()])
    submit = SubmitField("Отправить")


@app.route("/", methods=["GET", "POST"])
def index(name=None):
    form = SubscriptionForm()
    if request.method == "POST":
        name, email = request.form["name"], request.form["email"]
        sendEmail(app_password, name, email)
        return redirect(url_for("index"))

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
