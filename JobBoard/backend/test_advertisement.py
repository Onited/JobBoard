from fastapi.testclient import TestClient
from main import app
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import userModel
from baseModel import companyBase, advertisementBase
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


def test_create_advertisement(db: Session):
    advertisment = advertisementBase.AdvertisementBase(
        title = "string",
        ad_description = "string",
        job_type = "string",
        address = "string",
        salary = 0,
        company_id = 1,
    )
    response = client.post("/advertisement/create", json=advertisment.model_dump())
    assert response.status_code == 201


def test_get_advertisements(db: Session):
    response = client.get("advertisement/all")
    assert response.status_code == 200



def test_get_advertisement_by_city(db: Session):
    response = client.get("/advertisement/city/string")
    assert response.status_code == 200


def test_get_advertisement_by_job_type(db: Session):
    response = client.get("/advertisement/job_type/string")
    assert response.status_code == 200


def test_get_advertisement_by_city_not_found(db: Session):
    response = client.get("/advertisement/city/strings")
    assert response.status_code == 404
    assert response.json() == {"detail": "No advertisement found"}

def test_get_advertisement_by_job_type_not_found(db: Session):
    response = client.get("/advertisement/job_type/strings")
    assert response.status_code == 404
    assert response.json() == {"detail": "No advertisement found"}


def test_update_advertisement(db: Session):
    advertisement = advertisementBase.AdvertisementUpdate(
        title = "strings",
        ad_description = "strings",
        job_type = "strings",
        address = "strings",
        salary = 0,
    )
    response = client.put("/advertisement/update/1", json=advertisement.model_dump())
    assert response.status_code == 200

def test_update_advertisement_not_found(db: Session):
    advertisement = advertisementBase.AdvertisementUpdate(
        title = "strings",
        ad_description = "strings",
        job_type = "strings",
        address = "strings",
        salary = 0,
    )
    response = client.put("/advertisement/update/2", json=advertisement.model_dump())
    assert response.status_code == 404
    assert response.json() == {"detail": "Advertisement not found"}

def test_delete_advertisement(db: Session):
    response = client.delete("/advertisement/delete/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Advertisement deleted"}