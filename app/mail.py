from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from app.config import setting

mail_config = ConnectionConfig(
    MAIL_USERNAME = setting.MAIL_USERNAME,
    MAIL_PASSWORD = setting.MAIL_PASSWORD,
    MAIL_FROM = setting.MAIL_FROM,
    MAIL_PORT = setting.MAIL_PORT,
    MAIL_SERVER = setting.MAIL_SERVER,
    MAIL_FROM_NAME = setting.MAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

mail = FastMail(config=mail_config)

def create_message(recipients: list[EmailStr], subject: str, body: str):
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )
    
    return message