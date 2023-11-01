from pydantic import BaseModel

class AdvertisementBase(BaseModel):
    title: str
    ad_description: str
    job_type: str
    address: str
    salary: int
    company_id: int 

class Advertisement(AdvertisementBase):
    company_id: int
    company_name: str
    company_description: str | None = None


class AdvertisementUpdate(BaseModel):
    title: str | None = None
    ad_description: str | None = None
    job_type: str | None = None
    address: str | None = None
    salary: int | None = None