from fastapi.testclient import TestClient
from main import app
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import userModel
from baseModel import companyBase
import pytest

client = TestClient(app)


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def db():
    userModel.Base.metadata.create_all(bind=engine)
    yield override_get_db()
    userModel.Base.metadata.drop_all(bind=engine)


def test_create_company(db: Session):
    company = companyBase.CompanyBase(
        firstname="test",
        lastname="test",
        email="test@gmail.com",
        password="123456",
        company_name="test",
        siret="12345678912345",
    )
    response = client.post("/company/create", json=company.model_dump())
    assert response.status_code == 201
    assert response.json() == {"message": "Company created"}


def test_create_company_already_exist(db: Session):
    company = companyBase.CompanyBase(
        firstname="test",
        lastname="test",
        email="test@gmail.com",
        password="123456",
        company_name="test",
        siret="12345678912345",
    )
    response = client.post("/company/create", json=company.model_dump())
    assert response.status_code == 400
    assert response.json() == {"detail": "Company already exist"}


def test_get_companies(db: Session):
    response = client.get("/company/all")
    assert response.status_code == 200


def test_get_company(db: Session):
    response = client.get("/company/id/1")
    assert response.status_code == 200


def test_get_company_not_found(db: Session):
    response = client.get("/company/id/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Company not found"}


def test_auth_company(db: Session):
    response = client.get("/company/auth/test@gmail.com/123456")
    assert response.status_code == 200
    assert response.json() == {"message": "Authentification success"}


def test_auth_company_not_found(db: Session):
    response = client.get("/company/auth/oui@gmail.fr/123456")
    assert response.status_code == 404
    assert response.json() == {"detail": "Company not found"}


def test_auth_company_wrong_password(db: Session):
    response = client.get("/company/auth/test@gmail.com/1234567")
    assert response.status_code == 401
    assert response.json() == {"detail": "Wrong password"}


def test_update_company(db: Session):
    company = companyBase.updateCompanyBase(
        firstname="test2",
        lastname="test2"
    )
    response = client.put("/company/update/1", json=company.model_dump())
    assert response.status_code == 200


def test_update_company_not_found(db: Session):
    company = companyBase.updateCompanyBase(
        firstname="test2",
        lastname="test2"
    )
    response = client.put("/company/update/2", json=company.model_dump())
    assert response.status_code == 404
    assert response.json() == {"detail": "Company not found"}


def test_delete_company(db: Session):
    response = client.delete("/company/delete/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Company deleted"}


def test_delete_company_not_found(db: Session):
    response = client.delete("/company/delete/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "Company not found"}
