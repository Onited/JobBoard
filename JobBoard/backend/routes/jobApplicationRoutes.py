from fastapi import Depends, APIRouter, HTTPException, status
from typing import Annotated

from numpy import add
from database.database import SessionLocal
from sqlalchemy.orm import Session
from baseModel.jobApplicationBase import JobApplicationBase, JobApplicationUpdate, JobApplication
from models import jobApplicationModel


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix='/jobApplication')


def add_info(db_jobApplication, job_seeker, advertisement):
    db_jobApplication.job_seeker_firstname = job_seeker.firstname
    db_jobApplication.job_seeker_lastname = job_seeker.lastname
    db_jobApplication.advertisement_title = advertisement.title
    db_jobApplication.company_name = advertisement.company.company_name
    return db_jobApplication


@router.post("/create/", response_model=JobApplication, status_code=status.HTTP_201_CREATED)
async def create_jobApplication(jobApplication: JobApplicationBase, db: Session = Depends(get_db)):
    db_jobApplication = jobApplicationModel.JobApplication(**jobApplication.model_dump())
    jobSeeker = db.query(jobApplicationModel.JobSeeker).filter(jobApplicationModel.JobSeeker.jobSeeker_id == db_jobApplication.job_seeker_id).first()
    advertisement = db.query(jobApplicationModel.Advertisements).filter(jobApplicationModel.Advertisements.advertisements_id == db_jobApplication.advertisements_id).first()
    if jobSeeker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='JobSeeker not found')
    if advertisement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Advertisement not found')
    db.add(db_jobApplication)
    db.commit()
    db.refresh(db_jobApplication)
    add_info(db_jobApplication, jobSeeker, advertisement)
    return db_jobApplication


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_jobApplications(db: Session = Depends(get_db)):
    db_jobApplications = db.query(jobApplicationModel.JobApplication).all()
    for db_jobApplication in db_jobApplications:
        add_info(db_jobApplication, db_jobApplication.job_seeker, db_jobApplication.advertisements)
    return db_jobApplications


@router.get("/id/{job_application_id}", response_model=JobApplication, status_code=status.HTTP_200_OK)
async def get_jobApplication(job_application_id: int, db: Session = Depends(get_db)):
    db_jobApplication = db.query(jobApplicationModel.JobApplication).filter(
        jobApplicationModel.JobApplication.job_application_id == job_application_id).first()
    if db_jobApplication is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='JobApplication not found')
    add_info(db_jobApplication, db_jobApplication.job_seeker, db_jobApplication.advertisements)
    return db_jobApplication


@router.get("/job_seeker/{job_seeker_id}", response_model=list[JobApplication], status_code=status.HTTP_200_OK)
async def get_jobApplication_by_job_seeker(job_seeker_id: int, db: Session = Depends(get_db)):
    db_jobApplications = db.query(jobApplicationModel.JobApplication).filter(
        jobApplicationModel.JobApplication.job_seeker_id == job_seeker_id).all()
    if db_jobApplications == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='No jobApplication found')
    for db_jobApplication in db_jobApplications:
        add_info(db_jobApplication, db_jobApplication.job_seeker, db_jobApplication.advertisements)
    return db_jobApplications


@router.get("/advertisement/{advertisement_id}", response_model=list[JobApplication], status_code=status.HTTP_200_OK)
async def get_jobApplication_by_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    db_jobApplications = db.query(jobApplicationModel.JobApplication).filter(
        jobApplicationModel.JobApplication.advertisements_id == advertisement_id).all()
    if db_jobApplications == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='No jobApplication found')
    for db_jobApplication in db_jobApplications:
        add_info(db_jobApplication, db_jobApplication.job_seeker, db_jobApplication.advertisements)
    return db_jobApplications


@router.put("/update/{job_application_id}", response_model=JobApplication, status_code=status.HTTP_200_OK)
async def update_jobApplication(job_application_id: int, jobApplication: JobApplicationUpdate, db: Session = Depends(get_db)):
    db_jobApplication = db.query(jobApplicationModel.JobApplication).filter(
        jobApplicationModel.JobApplication.job_application_id == job_application_id).first()
    if db_jobApplication is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='JobApplication not found')
    for key, value in jobApplication.model_dump().items():
        if value is not None:
            setattr(db_jobApplication, key, value)
    db.commit()
    db.refresh(db_jobApplication)
    add_info(db_jobApplication, db_jobApplication.job_seeker, db_jobApplication.advertisements)
    return db_jobApplication


@router.delete("/delete/{job_application_id}", status_code=status.HTTP_200_OK)
async def delete_jobApplication(job_application_id: int, db: Session = Depends(get_db)):
    db_jobApplication = db.query(jobApplicationModel.JobApplication).filter(
        jobApplicationModel.JobApplication.job_application_id == job_application_id).first()
    if db_jobApplication is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='JobApplication not found')
    db.delete(db_jobApplication)
    db.commit()
    return {'message': 'JobApplication deleted'}