from pydantic import BaseModel, Field
from typing import Union


class User(BaseModel):
    username: str = Field(description="User-Name")
    email: str = Field(description="Email for the User")


class UserInDB(User):
    hashed_password: str = Field(description="Hased Password for the user")


class DateRangeQuery(BaseModel):
    date: Union[str, None] = Field(
        description="Date-Range that for which user wants the contact files",
        default=None,
        alias="date",
    )
