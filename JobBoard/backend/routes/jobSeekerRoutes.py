from fastapi import HTTPException, Depends, status, APIRouter
from typing import Annotated
from database.database import SessionLocal
from sqlalchemy.orm import Session
from baseModel.jobSeekerBase import JobSeekerBase, updateJobSeekerBase
from models import jobSeekerModel
from passlib.hash import sha256_crypt


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix='/jobSeeker')


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_jobSeeker(jobSeeker: JobSeekerBase, db: db_dependency):
    db_jobSeeker = jobSeekerModel.JobSeeker(**jobSeeker.model_dump())
    jobSeeker = db.query(jobSeekerModel.JobSeeker).filter(
        jobSeekerModel.JobSeeker.email == db_jobSeeker.email).first()
    if jobSeeker is None:
        db_jobSeeker.password = sha256_crypt.using(
            rounds=5000).hash(db_jobSeeker.password)
        db.add(db_jobSeeker)
        db.commit()
        return {'message': 'JobSeeker created'}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='JobSeeker already exist')


@router.get('/all', status_code=status.HTTP_200_OK)
async def get_jobSeekers(db: db_dependency):
    jobSeekers = db.query(jobSeekerModel.JobSeeker).all()
    return jobSeekers


@router.get('/id/{jobSeeker_id}', status_code=status.HTTP_200_OK)
async def get_jobSeeker(jobSeeker_id: int, db: db_dependency):
    jobSeeker = db.query(jobSeekerModel.JobSeeker).filter(
        jobSeekerModel.JobSeeker.jobSeeker_id == jobSeeker_id).first()
    if jobSeeker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='JobSeeker not found')
    return jobSeeker


@router.get('/auth/{email}/{password}', status_code=status.HTTP_200_OK)
async def auth_jobSeeker(email: str, password: str, db: db_dependency):
    jobSeeker = db.query(jobSeekerModel.JobSeeker).filter(
        jobSeekerModel.JobSeeker.email == email).first()
    if jobSeeker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='JobSeeker not found')
    if sha256_crypt.verify(password, jobSeeker.password) == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong password')
    return jobSeeker


@router.put('/update/{jobSeeker_id}', status_code=status.HTTP_200_OK)
async def update_jobSeeker(jobSeeker_id: int, jobSeeker_data: updateJobSeekerBase, db: db_dependency):
    db_jobSeeker = db.query(jobSeekerModel.JobSeeker).filter(
        jobSeekerModel.JobSeeker.jobSeeker_id == jobSeeker_id).first()
    if db_jobSeeker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='JobSeeker not found')

    for column, value in jobSeeker_data.model_dump().items():
        if value is not None:
            setattr(db_jobSeeker, column, value if column !=
                    'password' else sha256_crypt.using(rounds=5000).hash(value))

    db.commit()
    return {'message': 'JobSeeker updated'}


@router.delete('/delete/{jobSeeker_id}', status_code=status.HTTP_200_OK)
async def delete_jobSeeker(jobSeeker_id: int, db: db_dependency):
    db_jobSeeker = db.query(jobSeekerModel.JobSeeker).filter(
        jobSeekerModel.JobSeeker.jobSeeker_id == jobSeeker_id).first()
    if db_jobSeeker is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='JobSeeker not found')
    db.delete(db_jobSeeker)
    db.commit()
    return {'message': 'JobSeeker deleted'}
