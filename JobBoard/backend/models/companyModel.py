from sqlalchemy import Column, Integer, String, ForeignKey
from models.userModel import User

class Company(User):
    __tablename__ = 'company'
    
    company_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, index=True)
    company_name = Column(String(50), index=True)
    siret = Column(String(14), unique=True, index=True)
    description = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)