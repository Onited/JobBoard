from baseModel.userBase import UserBase, UserBaseUpdate

class JobSeekerBase(UserBase):
    genre: str
    birthdate: str | None = None
    cv: str | None = None


class updateJobSeekerBase(UserBaseUpdate):
    genre: str | None = None
    birthdate: str | None = None
    cv: str | None = None