# middlewares/__init__.py
from functools import wraps
import jwt
import os
import logging
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from models.all_models import User
from config.database import get_db
from dotenv import load_dotenv
from jwt import ExpiredSignatureError, InvalidTokenError


# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


def decode_jwt(token: str):
    """Decode and verify a JWT."""
    try:
        token = token.split(" ")[1]  # Split the 'Bearer <token>' format
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        logging.error("Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        logging.error("Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logging.error(f"Token decoding error: {e}")
        raise HTTPException(status_code=400, detail="Invalid authorization header")


def token_required(f):
    """Middleware to protect routes with token validation."""
    @wraps(f)
    async def decorated(*args, request: Request, db: Session = Depends(get_db), **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        decoded_data = decode_jwt(token)
        email = decoded_data.get("email")
        #email = "pavankumardandladsp@gmail.com"
        user = db.query(User).filter_by(email=email).first()
        logging.info(f"user_info {user}")

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return await f(user = user, db = db, *args, **kwargs)
 
    return decorated
