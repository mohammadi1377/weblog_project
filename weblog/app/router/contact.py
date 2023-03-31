# from fastapi import APIRouter, Form
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from pydantic import EmailStr
# from app.schema import ConnectionConfig
#
# router = APIRouter()
#
# conf = ConnectionConfig(
# 	MAIL_USERNAME="programtestingemail2@gmail.com",
# 	MAIL_PASSWORD="Ss*123456",
# 	MAIL_FROM="programtestingemail2@gmail.com",
# 	MAIL_PORT=587,
# 	MAIL_SERVER="smtp.gmail.com",
# 	MAIL_TLS=True,
# 	MAIL_SSL=False,
# 	MAIL_DEBUG=True,
# 	MAIL_STARTTLS=True,
# 	MAIL_SSL_TLS=False,
# )
#
# mail = FastMail(conf)
#
#
# @router.post("/contact-us")
# async def send_email(name: str = Form(...), email: EmailStr = Form(...), message: str = Form(...)):
#
#     message = MessageSchema(
#         subject=f"New message from {name}",
#         recipients=["programtestingemail2@gmail.com"],
#         body=f"Email: {email}\n\n{message}",
#         subtype="html"
#     )
#
#     await mail.send_message(message)
#     return {"message": "Email has been sent"}

from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
import smtplib
from email.mime.text import MIMEText

router = APIRouter()


@router.post("/contact-us")
async def contact_us(name: str = Form(...), email: str = Form(...), message: str = Form(...), to_email: str = Form(...)):
	sender_email = "f.mohamady1377@gmail.com"
	password = "59656046158233"

	msg = MIMEText(message)
	msg['Subject'] = f"{name} has sent you a message!"
	msg['From'] = sender_email
	msg['To'] = to_email

	try:
		# establish secure SSL connection to Gmail's SMTP server
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.login(sender_email, password)
		server.sendmail(sender_email, to_email, msg.as_string())
		server.quit()
		return PlainTextResponse("your message has been sent!")
	except Exception as e:
		return PlainTextResponse(f"An error occurred: {e}")

