import celery_app.config as config

from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType


mail_config = ConnectionConfig(
    MAIL_USERNAME=config.mail_username,
    MAIL_PASSWORD=config.mail_password,
    MAIL_FROM=config.mail_from,
    MAIL_FROM_NAME=config.mail_from_name,
    MAIL_SERVER=config.mail_server,
    MAIL_PORT=config.mail_port,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
)

mail = FastMail(config=mail_config)

def create_message(recipients: list, subject: str, body: str):
    return MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )
