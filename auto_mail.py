import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os

def mail_bot(path):
    sender_email = "gyanutiwari758@gmail.com"
    receiver_email = "2023281975.abhinav@ug.sharda.ac.in"
    password = "qynqulodegxqdhai"

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, password)

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "⚠️ Weapon Detected in Your Property"

        message.attach(MIMEText("A weapon has been detected. See attached image.", "plain"))

        with open(path, "rb") as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(path))
            part["Content-Disposition"] = f'attachment; filename="{os.path.basename(path)}"'
            message.attach(part)

        server.send_message(message)
        server.quit()
        print("✅ Email sent successfully.")

    except Exception as e:
        print(f"❌ Email sending failed: {e}")
