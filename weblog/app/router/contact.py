from fastapi import APIRouter, HTTPException
from fastapi_mail import FastMail, MessageSchema
from app.schema import ConnectionConfig
from app.schema import ContactForm

router = APIRouter()
conf = ConnectionConfig(
    MAIL_USERNAME="shervinrezaei1378@gmail.com",
    MAIL_PASSWORD="ansgarrjdwbmbeuc",
    MAIL_FROM="shervinrezaei1378@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    MAIL_DEBUG=True,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)
mail = FastMail(conf)


@router.post("/contact-us")
async def send_email(contact_form: ContactForm):
    message = MessageSchema(
        subject=f"New message from {contact_form.name}",
        recipients=[conf.MAIL_FROM],
        body=f"Email: {contact_form.email}\n\n{contact_form.message}",
        subtype="html"
    )

    try:
        response = await mail.send_message(message)
    except Exception as e:
        print("slm")
        raise HTTPException(status_code=500, detail="Error sending email")

    if response.status_code != 250:
        print("khodafez")
        raise HTTPException(status_code=501, detail="Error sending email")

    return {"message": "Email has been sent"}
