from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, MediaFile

DATABASE_URL = "sqlite:///media.db"

def create_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

def get_session():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()
