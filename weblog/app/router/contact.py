# from fastapi import APIRouter, HTTPException
# from fastapi_mail import FastMail, MessageSchema
# from fastapi.templating import Jinja2Templates
# from app.schema import ConnectionConfig
# from app.schema import ContactForm
#
#
# templates = Jinja2Templates(directory=".")
# router = APIRouter()
# conf = ConnectionConfig(
#     MAIL_USERNAME="shervinrezaei1378@gmail.com",
#     MAIL_PASSWORD="ansgarrjdwbmbeuc",
#     MAIL_FROM="shervinrezaei1378@gmail.com",
#     MAIL_PORT=587,
#     MAIL_SERVER="smtp.gmail.com",
#     MAIL_TLS=True,
#     MAIL_SSL=False,
#     MAIL_DEBUG=True,
#     MAIL_STARTTLS=True,
#     MAIL_SSL_TLS=False,
#     TEMPLATE_FOLDER='.',
#     template_engine=templates,
#
#
# )
# mail = FastMail(conf)
#
#
# @router.post("/contact-us")
# async def send_email(contact_form: ContactForm):
#     template = templates.get_template('contact.html')
#     message = MessageSchema(
#         subject=f"New message from {contact_form.name}",
#         recipients=[conf.MAIL_FROM],
#         body=f"Email: {contact_form.email}\n\n{contact_form.message}",
#         subtype="html"
#     )
#
#     try:
#         response = await mail.send_message(message, template_name=template)
#     except Exception as e:
#         print("slm")
#         raise HTTPException(status_code=500, detail=f"Error sending email{e}")
#
#     if response.status_code != 250:
#         print("khodafez")
#         raise HTTPException(status_code=501, detail="Error sending email")
#
#     return {"message": "Email has been sent"}

from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
import smtplib
from email.mime.text import MIMEText

router = APIRouter()


@router.post("/contact-us")
async def contact_us(name: str = Form(...), sender_email: str = Form(...), message: str = Form(...)):
	loginEmail = "shervinrezaei1378@gmail.com"
	password = "ansgarrjdwbmbeuc"

	msg = MIMEText(message)
	msg['Subject'] = f"{name} has sent you a message!"
	msg['From'] = sender_email
	msg['To'] = loginEmail

	try:
		# establish secure SSL connection to Gmail's SMTP server
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.login(loginEmail, password)
		server.sendmail(sender_email, loginEmail, msg.as_string())
		server.quit()
		return PlainTextResponse("your message has been sent to Us!")
	except Exception as e:
		return PlainTextResponse(f"An error occurred: {e}")
