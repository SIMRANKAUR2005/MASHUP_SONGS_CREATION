from flask import Flask, render_template, request
from mashup import create_mashup
import zipfile
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():

    singer = request.form["singer"]
    num = int(request.form["num"])
    duration = int(request.form["duration"])
    email = request.form["email"]

    output_file = f"{singer}_mashup.mp3"

    # create mashup
    path = create_mashup(singer, num, duration, output_file)

    # zip file
    zip_path = f"{path}.zip"

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(path)

    # send email
    msg = EmailMessage()
    msg['Subject'] = "Your Mashup File"
    msg['From'] = EMAIL
    msg['To'] = email

    msg.set_content("Mashup attached")

    with open(zip_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="zip", filename="mashup.zip")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)

    return "Mashup sent successfully to your email!"


if __name__ == "__main__":
    app.run(debug=True)