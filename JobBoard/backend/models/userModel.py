from sqlalchemy import Boolean, Column, Integer, String, DATE, LargeBinary
from database.database import Base

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    phone = Column(String(15), nullable=True)
    password = Column(String(100))
    city = Column(String(50), nullable=True)
    image_profile = Column(String(255), nullable=True)

