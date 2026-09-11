from app.shared.routes import create_router
from app.utils.decorators import exception_handler
from app.utils.mail import create_message, mail
from app.utils import http_utils

from .schemas import EmailModel

router = create_router("email")

@router.post('/send_email', summary="发送邮件")
@exception_handler("发送邮件")
async def send_email(emails: EmailModel):
    addresses = emails.addresses

    html = "<h1>Hello Email!</h1>"

    message = create_message(
        recipients=addresses,
        subject="Hello Email!",
        body=html
    )

    await mail.send_message(message)

    return http_utils.get_response(code=200, message="发送成功")
