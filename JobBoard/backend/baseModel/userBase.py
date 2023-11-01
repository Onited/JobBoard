from pydantic import BaseModel


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str
    phone: str | None = None
    city: str | None = None
    password: str
    image_profile: str | None = None


class UserBaseUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    city: str | None = None
    password: str | None = None
    image_profile: str | None = None