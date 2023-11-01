# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from models.jobSeekerModel import JobSeeker
# from models.companyModel import Company
# from models.advertisementsModel import Advertisements
# from database.database import Base

# class JobApplication(Base):
#     __tablename__ = 'job_application'
#     job_application_id = Column(Integer, primary_key=True, index=True)
#     job_application_status = Column(String(50), index=True)
#     job_application_date = Column(String(50), index=True)
#     job_application_message = Column(String(255), nullable=True)
#     job_application_cv = Column(String(255), nullable=True)
#     job_application_cover_letter = Column(String(255), nullable=True)
#     advertisements_id = Column(Integer, ForeignKey('advertisements.advertisements_id'), nullable=False)
#     advertisements = relationship("Advertisements", back_populates="job_application")
#     job_Seeker_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
#     job_Seeker = relationship("JobSeeker", back_populates="job_application")
#     company_id = Column(Integer, ForeignKey('company.company_id'), nullable=False)
#     company = relationship("Company", back_populates="job_application")

# Advertisements.job_application = relationship("JobApplication", back_populates="advertisements")
# JobSeeker.job_application = relationship("JobApplication", back_populates="job_Seeker")
# Company.job_application = relationship("JobApplication", back_populates="company")

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.jobSeekerModel import JobSeeker
from models.companyModel import Company
from models.advertisementsModel import Advertisements
from database.database import Base

class JobApplication(Base):
    __tablename__ = 'job_applications'
    job_application_id = Column(Integer, primary_key=True, index=True)
    job_application_status = Column(String(50), index=True)
    job_application_date = Column(String(50), index=True)
    job_application_message = Column(String(255), nullable=True)
    job_application_cv = Column(String(255), nullable=True)
    job_application_cover_letter = Column(String(255), nullable=True)
    advertisements_id = Column(Integer, ForeignKey('advertisements.advertisements_id'), nullable=False)
    advertisements = relationship("Advertisements", back_populates="job_applications")
    job_seeker_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    job_seeker = relationship("JobSeeker", back_populates="job_applications")
    company_id = Column(Integer, ForeignKey('company.company_id'), nullable=False)
    company = relationship(
        "Company", 
        back_populates="job_applications", 
        foreign_keys=[company_id]  # Spécification des clés étrangères
    )

Advertisements.job_applications = relationship("JobApplication", back_populates="advertisements")  # Adjusted to plural
JobSeeker.job_applications = relationship("JobApplication", back_populates="job_seeker")  # Adjusted to plural and snake_case
Company.job_applications = relationship("JobApplication", back_populates="company")  # Adjusted to plural
