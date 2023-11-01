from models.userModel import Base
from fastapi.testclient import TestClient
from main import app
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from models import userModel
from models.companyModel import Company
from models.advertisementsModel import Advertisements
from models.jobApplicationModel import JobApplication
from models.jobSeekerModel import JobSeeker
from baseModel import jobApplicationBase, jobSeekerBase, companyBase, advertisementBase
import pytest

client = TestClient(app)


@pytest.fixture(scope="module")
def db():
    userModel.Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        userModel.Base.metadata.drop_all(bind=engine)

def reset_database(db: Session):
    # Obtenez l'URL de la base de données à partir de la session
    url = db.get_bind().url

    # Créez une nouvelle connexion à la base de données
    engine = create_engine(url)

    # Exécutez une commande SQL pour supprimer toutes les tables
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))  # Désactivez la vérification des clés étrangères
        for table in Base.metadata.sorted_tables:  # Utilisez Base.metadata au lieu de db.metadata
            conn.execute(table.delete())
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

def company_fixture(db):
    new_job_seeker = JobSeeker(
        firstname= "John",
        lastname= "Doe",
        email= "john.doe@gmail.com",
        password= "examplepassword",
        genre= "male",
    )
    db.add(new_job_seeker)
    db.commit()
    job_seeker_id = new_job_seeker.jobSeeker_id
    db.close()
    # Create a new company
    new_company = Company(
        firstname="test",
        lastname="test",
        email="test@gmail.com",
        password="123456",
        company_name="test",
        siret="12345678912345",
    )
    db.add(new_company)
    db.commit()
    company_id = new_company.company_id
    db.close()
    
    new_advertisement = Advertisements(
        title = "string",
        ad_description = "string",
        job_type = "string",
        address = "string",
        salary = 0,
        company_id = company_id,
    )
    db.add(new_advertisement)
    db.commit()
    db.close()
    
    return [company_id, job_seeker_id]


def test_create_jobApplication(db: Session):
    reset_database(db)
    company_id = company_fixture(db)
    jobApplication = jobApplicationBase.JobApplicationBase(
        job_application_status = "string",
        job_application_date = "string",
        job_application_message = "string",
        job_application_cv = "string",
        job_application_cover_letter = "string",
        advertisements_id = 1,
        job_seeker_id = 1,
        company_id = company_id[0],
    )
    response = client.post("/jobApplication/create", json=jobApplication.model_dump())
    assert response.status_code == 201


def test_get_jobApplications(db: Session):
    response = client.get("/jobApplication/all")
    assert response.status_code == 200


def test_get_jobApplication(db: Session):
    response = client.get("/jobApplication/id/1")
    assert response.status_code == 200


def test_get_jobApplication_not_found(db: Session):
    response = client.get("/jobApplication/id/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "JobApplication not found"}


def test_get_jobApplication_by_job_seeker(db: Session):
    response = client.get("/jobApplication/job_seeker/1")
    assert response.status_code == 200


def test_get_jobApplication_by_job_seeker_not_found(db: Session):
    response = client.get("/jobApplication/job_seeker/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "No jobApplication found"}


def test_get_jobApplication_by_advertisement(db: Session):
    response = client.get("/jobApplication/advertisement/1")
    assert response.status_code == 200


def test_get_jobApplication_by_advertisement_not_found(db: Session):
    response = client.get("/jobApplication/advertisement/2")
    assert response.status_code == 404
    assert response.json() == {"detail": "No jobApplication found"}


def test_update_jobApplication(db: Session):
    jobApplication = jobApplicationBase.JobApplicationUpdate(
        job_application_status = "strings",
        job_application_date = "strings",
        job_application_message = "strings",
        job_application_cv = "strings",
        job_application_cover_letter = "strings",
    )
    response = client.put("/jobApplication/update/1", json=jobApplication.model_dump())
    assert response.status_code == 200


def test_update_jobApplication_not_found(db: Session):
    jobApplication = jobApplicationBase.JobApplicationUpdate(
        job_application_status = "strings",
        job_application_date = "strings",
        job_application_message = "strings",
        job_application_cv = "strings",
        job_application_cover_letter = "strings",
    )
    response = client.put("/jobApplication/update/2", json=jobApplication.model_dump())
    assert response.status_code == 404
    assert response.json() == {"detail": "JobApplication not found"}


def test_delete_jobApplication(db: Session):
    response = client.delete("/jobApplication/delete/1")
    assert response.status_code == 200
    assert response.json() == {"message": "JobApplication deleted"}
