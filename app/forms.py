from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class SubscriptionForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    email = StringField("Электронная почта", validators=[DataRequired()])
    submit = SubmitField("Отправить")
