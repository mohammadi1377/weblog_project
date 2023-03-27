from fastapi import APIRouter, Form
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

router = APIRouter()

conf = ConnectionConfig(
    MAIL_USERNAME="programtestingemail2@gmail.com",
    MAIL_PASSWORD="Ss*123456",
    MAIL_FROM="programtestingemail2@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False
)

mail = FastMail(conf)


@router.post("/contact-us")
async def send_email(name: str = Form(...), email: EmailStr = Form(...), message: str = Form(...)):

    message = MessageSchema(
        subject=f"New message from {name}",
        recipients=["programtestingemail2@gmail.com"],
        body=f"Email: {email}\n\n{message}",
        subtype="html"
    )

    await mail.send_message(message)
    return {"message": "Email has been sent"}