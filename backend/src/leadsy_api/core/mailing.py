from pathlib import Path
from typing import Any

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from leadsy_api.core.config import get_settings

configuration = ConnectionConfig(
    MAIL_USERNAME=get_settings().mail_username,
    MAIL_PASSWORD=get_settings().mail_password,
    MAIL_FROM=get_settings().mail_from_address,
    MAIL_PORT=get_settings().mail_port,
    MAIL_SERVER=get_settings().mail_host,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "emails",
)


mailer = FastMail(configuration)


async def send_email(
    *,
    recipient: str,
    subject: str,
    template_name: str,
    data: dict[str, Any],
) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        template_body=data,
        subtype=MessageType.html,
    )

    await mailer.send_message(message, template_name=template_name)
