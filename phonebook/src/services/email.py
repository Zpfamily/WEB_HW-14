from pathlib import Path
from dotenv import load_dotenv
import os

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import auth_service


load_dotenv()
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "youruser@meta.ua"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "yourpassword"),
    MAIL_FROM=os.getenv("MAIL_USERNAME", "youruser@meta.ua"),
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    The send_email function sends an email to the user with a link to confirm their email address.
        The function takes in three arguments:
            -email: the user's email address, which is used as a unique identifier for them.
            -username: the username of the user who is registering. This will be displayed in 
                their confirmation message so they know it was sent to them and not someone else.
            -host: this is where we are hosting our application, which will be used as part of 
                our confirmation link.
    
    :param email: EmailStr: Validate the email address
    :param username: str: Pass the username to the template
    :param host: str: Create the link for the user to confirm their email address
    :return: A coroutine object
    :doc-author: Trelent
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")
    except ConnectionErrors as err:
        print(err)

