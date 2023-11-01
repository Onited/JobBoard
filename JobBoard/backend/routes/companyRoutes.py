from fastapi import HTTPException, Depends, status, APIRouter
from typing import Annotated
from database.database import SessionLocal
from sqlalchemy.orm import Session
from baseModel.companyBase import CompanyBase, updateCompanyBase
from models import companyModel
from passlib.hash import sha256_crypt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix='/company')

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_company(company: CompanyBase, db: db_dependency):
    db_company = companyModel.Company(**company.model_dump())
    company = db.query(companyModel.Company).filter(
        companyModel.Company.email == db_company.email).first()
    if company is None:
        db_company.password = sha256_crypt.using(
            rounds=5000).hash(db_company.password)
        db.add(db_company)
        db.commit()
        return {'message': 'Company created'}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Company already exist')


@router.get('/all', status_code=status.HTTP_200_OK)
async def get_companies(db: db_dependency):
    companies = db.query(companyModel.Company).all()
    return companies


@router.get('/id/{company_id}', status_code=status.HTTP_200_OK)
async def get_company(company_id: int, db: db_dependency):
    company = db.query(companyModel.Company).filter(
        companyModel.Company.company_id == company_id).first()
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
    return company


@router.get('/auth/{email}/{password}', status_code=status.HTTP_200_OK)
async def auth_company(email: str, password: str, db: db_dependency):
    company = db.query(companyModel.Company).filter(
        companyModel.Company.email == email).first()
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
    if sha256_crypt.verify(password, company.password):
        return {'message': 'Authentification success'}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Wrong password')


@router.put('/update/{company_id}', status_code=status.HTTP_200_OK)
async def update_company(company_id: int, company: updateCompanyBase, db: db_dependency):
    db_company = db.query(companyModel.Company).filter(
        companyModel.Company.company_id == company_id).first()
    if db_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
    for key, value in company.model_dump().items():
        if value is not None:
            setattr(db_company, key, value)
    db.commit()
    return {'message': 'Company updated'}

@router.delete('/delete/{company_id}', status_code=status.HTTP_200_OK)
async def delete_company(company_id: int, db: db_dependency):
    db_company = db.query(companyModel.Company).filter(
        companyModel.Company.company_id == company_id).first()
    if db_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Company not found')
    db.delete(db_company)
    db.commit()
    return {'message': 'Company deleted'}