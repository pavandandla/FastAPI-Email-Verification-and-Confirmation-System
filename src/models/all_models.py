

from sqlalchemy import Column, Integer, String, Boolean, DateTime
#from sqlalchemy.ext.declarative import declarative_base
from config.database import Base
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users_info"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
 
    def set_password(self, password: str):
        
        #Hash the given password and store it in the database.
        
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        
        #Verify a given password against the stored hashed password.
    
        return pwd_context.verify(password, self.hashed_password)

    def to_dict(self):
        
        #Convert the user object to a dictionary.
        
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat(),
        }
