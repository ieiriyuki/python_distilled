import smtplib
from email.message import EmailMessage

from_addr = "ieiri.yuki@mfkessai.co.jp"
to_addr = "ieiri.yuki@moneyforward.co.jp"
subject = "title"
body = "hello world"
message = EmailMessage()
message["From"] = from_addr
message["To"] = to_addr
message["Subject"] = subject
message.set_content(body)
with smtplib.SMTP("localhost") as smtp:
    smtp.send_message(message)
