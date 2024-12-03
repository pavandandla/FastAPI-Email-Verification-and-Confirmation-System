# controllers/user_controller.py
"""from fastapi import Depends, Request
from sqlalchemy.orm import Session
from config.database import get_db
from middlewares import token_required
from config.config import create_app # Assuming app is defined and accessible
from models.all_models import User
from services.user_services import (
    signup_service,
    confirm_user_service,
    send_email_password_reset_service,
    update_password_service,
    login_service
)

app=create_app()


async def signup(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    response = await signup_service(data, db , app.state.mail_config)
    return response


async def confirm_user(token: str, db: Session = Depends(get_db)):
    response = await confirm_user_service(token, db)
    return response

async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    response = await login_service(data, db)
    return response
 
@token_required
async def send_email_password_reset(request: Request, user: dict ,db: Session = Depends(get_db)):
    email= user['email']
    response = await send_email_password_reset_service(email, db)
    return response

async def update_password(token: str, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    response = await update_password_service(token, data, db)
    return response"""

from fastapi import  Depends, Request, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from middlewares import token_required
from config.config import create_app
from models.all_models import User
from middlewares import decode_jwt
from services.user_services import (
    signup_service,
    confirm_user_service,
    send_email_password_reset_service,
    update_password_service,
    login_service
)
import logging

app=create_app()


async def signup(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    response = await signup_service(data, db, app.state.mail_config)
    return response


async def confirm_user(token: str, db: Session = Depends(get_db)):
    response = await confirm_user_service(token, db)
    return response


async def login(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    response = await login_service(data, db)
    return response

async def send_email_password_reset(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("Authorization")
    if not token:
            raise HTTPException(status_code=401, detail="Authorization header missing")
    
    decoded_data = decode_jwt(token)
    email = decoded_data.get("email")
    response = await send_email_password_reset_service(email, db, app.state.mail_config)
    return response


async def update_password(token: str, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    response = await update_password_service(token, data, db)
    return response

