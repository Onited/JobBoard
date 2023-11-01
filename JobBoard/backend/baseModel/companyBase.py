from baseModel.userBase import UserBase, UserBaseUpdate

class CompanyBase(UserBase):
    company_name: str
    siret: str
    description: str | None = None
    address: str | None = None

class updateCompanyBase(UserBaseUpdate):
    company_name: str | None = None
    siret: str | None = None
    description: str | None = None
    address: str | None = None