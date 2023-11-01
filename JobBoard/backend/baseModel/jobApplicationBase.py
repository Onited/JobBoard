from pydantic import BaseModel

class JobApplicationBase(BaseModel):
    job_application_status: str
    job_application_date: str
    job_application_message: str | None = None
    job_application_cv: str | None = None
    job_application_cover_letter: str | None = None
    advertisements_id: int
    job_seeker_id: int
    company_id: int

class JobApplication(JobApplicationBase):
    advertisements_id: int
    advertisement_title: str
    job_seeker_id: int
    job_seeker_firstname: str
    job_seeker_lastname: str
    company_id: int
    company_name: str

class JobApplicationUpdate(BaseModel):
    job_application_status: str | None = None
    job_application_date: str | None = None
    job_application_message: str | None = None
    job_application_cv: str | None = None
    job_application_cover_letter: str | None = None