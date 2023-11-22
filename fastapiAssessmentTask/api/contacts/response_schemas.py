from pydantic import BaseModel, Field
from typing import List


class SuccessRespose(BaseModel):
    detail: str = Field(description="Success Message")


class ErrorResponse(BaseModel):
    detail: str = Field(description="Error Message")


class Token(BaseModel):
    access_token: str = Field(description="Access Token")
    token_type: str = Field(description="Token Type")


class ContactSingleFile(BaseModel):
    uid: str = Field(description="Uniquely Identifies the Contact File", alias="uid")
    filename: str = Field(description="Uploaded File Name", alias="fileName")
    upload_date: str = Field(
        description="Date at which file was uploaded", alias="uploadDate"
    )
    total_contacts: int = Field(
        description="Total Number of Contacts in the File", alias="totalContacts"
    )


class ContactFile(BaseModel):
    uid: str = Field(description="Uniquely Identifies the Contact File", alias="uid")
    upload_date: str = Field(
        description="Date at which file was uploaded", alias="uploadDate"
    )
    total_contacts: int = Field(
        description="Total Number of Contacts in the File", alias="totalContacts"
    )


class ContactFileResponseList(BaseModel):
    contacts: List[ContactFile] = Field(
        description="A List consisting of information about each contact file"
    )
    total_contacts: int = Field(
        description="Total Number of Contacts Files", alias="totalContacts"
    )
