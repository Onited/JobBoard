from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.companyModel import Company
from database.database import Base


class Advertisements(Base):
    __tablename__ = 'advertisements'
    advertisements_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    ad_description = Column(String(255), nullable=True)
    job_type = Column(String(50), index=True)  # CDI, Stage, etc.
    address = Column(String(255), nullable=True)
    salary = Column(Integer, nullable=True)
    company_id = Column(Integer, ForeignKey('company.company_id'), nullable=False)
    company = relationship("Company", back_populates="advertisements")

Company.advertisements = relationship("Advertisements", back_populates="company")