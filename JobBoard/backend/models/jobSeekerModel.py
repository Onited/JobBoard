from sqlalchemy import Column, Integer, String, ForeignKey
from models.userModel import User

class JobSeeker(User):
    __tablename__ = 'job_seeker'
    
    jobSeeker_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, index=True)
    genre = Column(String(10))
    cv = Column(String(255), nullable=True)
    birthdate = Column(String(10), nullable=True)