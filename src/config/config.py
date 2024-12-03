from fastapi import FastAPI
import os
from dotenv import load_dotenv
from datetime import timedelta
from fastapi_mail import ConnectionConfig

load_dotenv()

def create_app():
    app = FastAPI()

    # Setup application configurations
    app.state.mail_config = ConnectionConfig(
        MAIL_USERNAME ="dandlapavankumar@gmail.com",
        MAIL_PASSWORD = "pijd nzcp ajoe qjxp",
        MAIL_FROM = "dandlapavankumar@gmail.com",
        MAIL_PORT = 465,
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_STARTTLS = False,
        MAIL_SSL_TLS = True,
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
    )

    # Other configurations
    app.state.secret_key = os.getenv("SECRET_KEY")
    app.state.jwt_secret_key = os.getenv("JWT_SECRET_KEY")
    app.state.jwt_expiration = timedelta(minutes=5)

    return app
 