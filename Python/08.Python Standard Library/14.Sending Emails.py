from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
import smtplib
from getpass import getpass

message = MIMEMultipart()
sender = "ryandouchangxu@gmail.com"
message["from"] = sender
message["to"] = "ryandouchangxu@gmail.com"
message["subject"] = "Das ist eine Überraschung"
message.attach(MIMEText("Body"))
message.attach(MIMEImage(Path("Image.png").read_bytes()))

app_password = getpass("请输入 Google 应用专用密码：")

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(sender, app_password)
    smtp.send_message(message)
    print("Sent...")
