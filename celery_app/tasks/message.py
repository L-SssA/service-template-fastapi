import asyncio

from loguru import logger
from celery import shared_task

from celery_app.utils.mail import create_message, mail

@shared_task(name="celery_app.tasks.message.send_message")
def send_message(recipients: list, subject: str, body: str) -> int:
    message = create_message(recipients, subject, body)

    asyncio.run(mail.send_message(message=message))

    logger.success(f"邮件发送到 {recipients} 用户成功")
