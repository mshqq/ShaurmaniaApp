import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template


sender = "miahasik@gmail.com"


def sendEmail(app_password, name, email):
    html = render_template("email_subscription.html", name=name)

    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = email
    msg["Subject"] = "Подписка на рассылку"
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.send_message(msg)

    print("Письмо отправлено!")
