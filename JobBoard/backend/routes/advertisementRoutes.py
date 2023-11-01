from fastapi import Depends, APIRouter, HTTPException, status
from typing import Annotated
from database.database import SessionLocal
from sqlalchemy.orm import Session
from baseModel.advertisementBase import Advertisement, AdvertisementBase, AdvertisementUpdate
from models import advertisementsModel


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix='/advertisement')


@router.post("/create/", response_model=Advertisement, status_code=status.HTTP_201_CREATED)
async def create_advertisement(advertisement: AdvertisementBase, db: Session = Depends(get_db)):
    db_advertisement = advertisementsModel.Advertisements(**advertisement.model_dump())
    company = db.query(advertisementsModel.Company).filter(advertisementsModel.Company.company_id == db_advertisement.company_id).first() 
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)
    db_advertisement.company_description = db_advertisement.company.description
    db_advertisement.company_name = db_advertisement.company.company_name
    return db_advertisement


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_advertisements(db: Session = Depends(get_db)):
    db_advertisements = db.query(advertisementsModel.Advertisements).all()
    for db_advertisement in db_advertisements:
        db_advertisement.company_description = db_advertisement.company.description
        db_advertisement.company_name = db_advertisement.company.company_name
    return db_advertisements


@router.get("/city/{city}", response_model=list[Advertisement], status_code=status.HTTP_200_OK)
async def get_advertisement_by_city(city: str, db: Session = Depends(get_db)):
    db_advertisements = db.query(advertisementsModel.Advertisements).filter(
        advertisementsModel.Advertisements.address.contains(city)).all()
    if db_advertisements == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='No advertisement found')
    for db_advertisement in db_advertisements:
        db_advertisement.company_description = db_advertisement.company.description
        db_advertisement.company_name = db_advertisement.company.company_name
    return db_advertisements


@router.get("/job_type/{job_type}", response_model=list[Advertisement], status_code=status.HTTP_200_OK)
async def get_advertisement_by_job_type(job_type: str, db: Session = Depends(get_db)):
    db_advertisements = db.query(advertisementsModel.Advertisements).filter(
        advertisementsModel.Advertisements.job_type == job_type).all()
    if db_advertisements == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='No advertisement found')
    for db_advertisement in db_advertisements:
        db_advertisement.company_description = db_advertisement.company.description
        db_advertisement.company_name = db_advertisement.company.company_name
    return db_advertisements


@router.get("/company/{company_name}", response_model=list[Advertisement], status_code=status.HTTP_200_OK)
async def get_advertisement_by_company(company_name: str, db: Session = Depends(get_db)):
    db_advertisements = db.query(advertisementsModel.Advertisements).join(advertisementsModel.Company).filter(
        advertisementsModel.Company.company_name == company_name).all()
    if db_advertisements == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='No advertisement found')
    for db_advertisement in db_advertisements:
        db_advertisement.company_description = db_advertisement.company.description
        db_advertisement.company_name = db_advertisement.company.company_name
    return db_advertisements


@router.put("/update/{advertisement_id}", response_model=Advertisement, status_code=status.HTTP_200_OK)
async def update_advertisement(advertisement_id: int, advertisement: AdvertisementUpdate, db: Session = Depends(get_db)):
    db_advertisement = db.query(advertisementsModel.Advertisements).filter(
        advertisementsModel.Advertisements.advertisements_id == advertisement_id).first()
    if db_advertisement == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Advertisement not found')
    for var, value in vars(advertisement).items():
        if value is not None:
            setattr(db_advertisement, var, value)
    db.commit()
    db.refresh(db_advertisement)
    db_advertisement.company_description = db_advertisement.company.description
    db_advertisement.company_name = db_advertisement.company.company_name
    return db_advertisement


@router.delete("/delete/{advertisement_id}", status_code=status.HTTP_200_OK)
async def delete_advertisement(advertisement_id: int, db: Session = Depends(get_db)):
    db_advertisement = db.query(advertisementsModel.Advertisements).filter(
        advertisementsModel.Advertisements.advertisements_id == advertisement_id).first()
    if db_advertisement == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Advertisement not found')
    db.delete(db_advertisement)
    db.commit()
    return {'message': 'Advertisement deleted'}
