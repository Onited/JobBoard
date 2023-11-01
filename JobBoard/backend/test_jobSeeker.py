from fastapi.testclient import TestClient
from main import app
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import userModel
from baseModel import jobSeekerBase
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


def test_create_jobSeeker(db: Session):
    jobSeeker = jobSeekerBase.JobSeekerBase(
        firstname= "string",
        lastname= "string",
        email= "string@gmail.com",
        password= "string",
        genre= "string",
    )
    response = client.post("/jobSeeker/create", json=jobSeeker.model_dump())
    assert response.status_code == 201
    assert response.json() == {"message": "JobSeeker created"}

def test_create_jobSeeker_already_exist(db: Session):
    jobSeeker = jobSeekerBase.JobSeekerBase(
        firstname= "string",
        lastname= "string",
        email= "string@gmail.com",
        password= "string",
        genre= "string",
    )
    response = client.post("/jobSeeker/create", json=jobSeeker.model_dump())
    assert response.status_code == 400
    assert response.json() == {"detail": "JobSeeker already exist"}


def test_get_jobSeekers(db: Session):
    response = client.get("/jobSeeker/all")
    assert response.status_code == 200


def test_get_jobSeeker(db: Session):
    response = client.get("/jobSeeker/id/1")
    assert response.status_code == 200


def test_auth_jobSeeker(db: Session):
    response = client.get("/jobSeeker/auth/string@gmail.com/string")
    assert response.status_code == 200


def test_auth_jobSeeker_not_found(db: Session):
    response = client.get("/jobSeeker/auth/strings@gmail.com/string")
    assert response.status_code == 404
    assert response.json() == {"detail": "JobSeeker not found"}


def test_auth_jobSeeker_wrong_password(db: Session):
    response = client.get("/jobSeeker/auth/string@gmail.com/strings")
    assert response.status_code == 401
    assert response.json() == {"detail": "Wrong password"}


def test_update_jobSeeker(db: Session):
    jobSeeker = jobSeekerBase.JobSeekerBase(
        firstname= "strings",
        lastname= "strings",
        email= "strings@gmail.com",
        password= "strings",
        genre= "strings",
    )
    response = client.put("/jobSeeker/update/1", json=jobSeeker.model_dump())
    assert response.status_code == 200
    assert response.json() == {"message": "JobSeeker updated"}

def test_update_jobSeeker_not_found(db: Session):
    jobSeeker = jobSeekerBase.JobSeekerBase(
        firstname= "strings",
        lastname= "strings",
        email= "string@gmail.com",
        password= "strings",
        genre= "strings",
    )
    response = client.put("/jobSeeker/update/2", json=jobSeeker.model_dump())
    assert response.status_code == 404
    assert response.json() == {"detail": "JobSeeker not found"}

def test_delete_jobSeeker(db: Session):
    response = client.delete("/jobSeeker/delete/1")
    assert response.status_code == 200