from app.shared.routes import create_router
from app.utils.decorators import exception_handler
from app.utils import http_utils
from app.utils.celery_client import celery_client

from .schemas import EmailModel, SendEmailResponse

router = create_router("email")

@router.post('/send_email', summary="发送邮件", response_model=SendEmailResponse)
@exception_handler("发送邮件")
async def send_email(
    emails: EmailModel,
):
    celery_client.send_task(
        "celery_app.tasks.message.send_message",
        kwargs={
            "recipients": emails.addresses,
            "subject": "Hello Email!",
            "body": "<h1>Hello Email!</h1>"
        }
    )
    return http_utils.get_response(code=200, message="发送成功")
