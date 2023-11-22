from pydantic import BaseModel, Field


class Contact(BaseModel):
    first_name: str = Field(description="First name of contact", alias="firstName")
    last_name: str = Field(description="Last name of contact", alias="lastName")
    company_name: str = Field(
        description="Company name of contact", alias="companyName"
    )
    email: str = Field(description="Email of contact", alias="email")
