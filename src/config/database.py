from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load database URL from environment variables
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

# SQLAlchemy engine and session setup
#engine = create_engine(SQLALCHEMY_DATABASE_URI, future=True)
engine = create_engine('mysql+pymysql://root:Pavan%4012@localhost/registration')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Function to initialize the database and create tables
def init_db() -> None:
    Base.metadata.create_all(bind=engine)

# Dependency to get a database session for request handling
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
