# services/user_services.py

from fastapi_mail import FastMail, MessageSchema, MessageType
from models.all_models import User
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
import os
from config.config import create_app
from dotenv import load_dotenv
from middlewares import decode_jwt

load_dotenv()
# Create app and initialize mail configuration
app = create_app()
mail_config = app.state.mail_config
fm = FastMail(mail_config)


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT
SECRET_KEY = os.getenv("SECRET_KEY")

async def signup_service(data, db: Session, mail_config: dict):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return JSONResponse({"status": "Success", "Statuscode": 400, "message": "All fields are required"}, status_code=400)

    user = db.query(User).filter_by(email=email).first()
    if user:
        return JSONResponse({"status": "Success","Statuscode": 200, "message": "User already exists"}, status_code=200)

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.add(new_user)
    db.commit()

    expiration_time = datetime.utcnow() + timedelta(hours=1)
    token_data = {"email": email, "exp": expiration_time}
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")

    confirmation_url = f"http://127.0.0.1:8000/confirm-user/{token}"
    message = MessageSchema(
        subject="Confirm Your Email",
        recipients=[new_user.email],
        body=f"Welcome {new_user.username}, confirm your email here: {confirmation_url}",
        subtype=MessageType.html
    )
    await fm.send_message(message)

    return JSONResponse({"status": "success","Statuscode": 201, "message": "User created. Check your email for confirmation."}, status_code=201)


async def confirm_user_service(token: str, db: Session):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = data.get("email")

        user = db.query(User).filter_by(email=email).first()
        if not user:
            return JSONResponse({"status": "Success","Statuscode": 200, "message": "User not found"}, status_code=200)

        user.is_verified = True
        db.commit()
        return JSONResponse({"status": "success", "message": "Email verified successfully"}, status_code=200)
    except jwt.ExpiredSignatureError:
        return JSONResponse({"status": "failed","Statuscode": 400, "message": "Token expired"}, status_code=400)
    except jwt.InvalidTokenError:
        return JSONResponse({"status": "failed","Statuscode": 400, "message": "Invalid token"}, status_code=400)


async def login_service(data: dict, db: Session):
    email = data.get("email")
    password = data.get("password")

    user = db.query(User).filter_by(email=email).first()
    if not user:
        return JSONResponse({"status": "Success","Statuscode": 200 ,"message": "User not found"}, status_code=200)

    if not user.verify_password(password):
        return JSONResponse({"status": "Success", "Statuscode": 401, "message": "Incorrect password"}, status_code=401)

    if not user.is_verified:
        return JSONResponse({"status": "Success","Statuscode": 200, "message": "Please verify your email"}, status_code=200)

    token_data = {"email": user.email, "exp": datetime.utcnow() + timedelta(hours=1)}
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")

    return JSONResponse({"status": "success","Statuscode": 200, "message": "Login successful", "token": token}, status_code=200)


async def send_email_password_reset_service(email: str, db: Session, mail_config: dict):
    user = db.query(User).filter_by(email=email).first()
    if not user:
        return JSONResponse({"status": "Success","Statuscode": 200, "message": "User not found"}, status_code=200)

    expiration_time = datetime.utcnow() + timedelta(minutes=30)
    token_data = {"email": email, "exp": expiration_time}
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")

    reset_url = f"http://127.0.0.1:8000/update-password/{token}"
    message = MessageSchema(
        subject="Reset Your Password",
        recipients=[user.email],
        body=f"Hi {user.username}, reset your password here: {reset_url}",
        subtype=MessageType.html
    )
    await fm.send_message(message)

    return JSONResponse({"status": "success","Statuscode": 200, "message": "Password reset email sent"}, status_code=200)


async def update_password_service(token: str, data: dict, db: Session):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = token_data.get("email")

        user = db.query(User).filter_by(email=email).first()
        if not user:
            return JSONResponse({"status": "success","Statuscode": 200, "message": "User not found"}, status_code=200)

        new_password = data.get("new_password")
        if not new_password:
            return JSONResponse({"status": "success","Statuscode": 400, "message": "New password is required"}, status_code=400)

        user.set_password(new_password)
        db.commit()
        return JSONResponse({"status": "success","Statuscode": 200, "message": "Password updated successfully"}, status_code=200)
    except jwt.ExpiredSignatureError:
        return JSONResponse({"status": "failed","Statuscode": 400, "message": "Token expired"}, status_code=400)
    except jwt.InvalidTokenError:
        return JSONResponse({"status": "failed","Statuscode": 400, "message": "Invalid token"}, status_code=400)
