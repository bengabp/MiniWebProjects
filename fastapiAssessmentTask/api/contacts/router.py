from typing import Annotated
from api.contacts.request_schemas import User, UserInDB, DateRangeQuery
from api.contacts.response_schemas import (
    SuccessRespose,
    ErrorResponse,
    Token,
    ContactFileResponseList,
    ContactSingleFile,
)
from api.contacts import (
    is_valid_csv,
    parse_csv,
    save_contacts_to_database,
    get_current_user,
    fake_hash_password,
    get_contact_files_associated_with_users,
    fetch_contact_by_uid,
    get_csv_data,
    delete_validate_contact,
)
from api.config import FAKE_USERS_DB
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import UploadFile, File, status, Depends, FastAPI, HTTPException, status
from fastapi.responses import Response
import pandas as pd

app = FastAPI()


@app.post(
    "/token",
    tags=["Token"],
    summary="Gets token for the user",
    responses={
        status.HTTP_200_OK: {"model": Token},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
    },
)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = FAKE_USERS_DB.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


@app.post(
    "/upload",
    tags=["Upload-Contacts"],
    summary="Extract Contact Information from uploaded CSV File and Store data on underlying Database",
    responses={
        status.HTTP_200_OK: {"model": SuccessRespose},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ErrorResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
def upload_csv_and_parse_data(
    current_user: Annotated[User, Depends(get_current_user)],
    file: UploadFile = File(...),
):
    filename = file.filename
    # Check if the uploaded file is a valid CSV
    response = is_valid_csv(file)
    if not isinstance(response, pd.DataFrame):
        raise HTTPException(status_code=422, detail="Invalid CSV File")

    # Parse the CSV file and extract contact information
    contacts_data = parse_csv(response)

    # # Save the extracted contacts to the database
    save_contacts_to_database(current_user.email, filename, contacts_data)

    return SuccessRespose(
        detail="Your CSV file has been uploaded to the underlying database"
    )


@app.get(
    "/contacts",
    tags=["Get-Contacts"],
    summary="Get Contacts by Date Range",
    responses={
        status.HTTP_200_OK: {"model": ContactFileResponseList},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
def get_contacts_by_date_range(
    date_range: Annotated[DateRangeQuery, Depends(DateRangeQuery)],
    user: Annotated[User, Depends(get_current_user)],
):
    response = get_contact_files_associated_with_users(user.email, date_range.date)
    if response == "No Contact Files":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact Files not found"
        )
    if response:
        return response
    else:
        raise HTTPException(
            status_code=400,
            detail="Please provide the date-range in the correct format",
        )


@app.get(
    "/contacts/{uid}",
    tags=["Get-Contact"],
    summary="Get Contact by UID",
    responses={
        status.HTTP_200_OK: {"model": ContactSingleFile},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
def get_contact_by_uid(
    uid: str,
    user: User = Depends(get_current_user),
):
    # Fetch contact information by UID from the database
    contact_info = fetch_contact_by_uid(user.email, uid)
    if not contact_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact File not found"
        )
    return contact_info


@app.get(
    "/contacts/{uid}/download",
    tags=["Download-Contacts"],
    summary="Download Contact File",
    responses={
        status.HTTP_200_OK: {"model": str, "description": "CSV-String"},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
def download_contact_file(
    uid: str,
    user: User = Depends(get_current_user),
):
    # Check if the contact file exists and belongs to the user
    response_data = get_csv_data(user.email, uid)

    if not response_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact file not found"
        )
    response = Response(content=response_data["data"], media_type="text/csv")
    response.headers[
        "Content-Disposition"
    ] = f"attachment; filename={response_data['name']}"
    # Provide the contact file for download
    return response


@app.delete(
    "/contacts/{uid}",
    tags=["Delete-Contacts"],
    summary="Delete Contact File",
    responses={
        status.HTTP_200_OK: {"model": SuccessRespose},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse},
    },
)
def delete_contact_file(
    uid: str,
    user: User = Depends(get_current_user),
):
    # Check if the contact file exists and belongs to the user
    response = delete_validate_contact(user.email, uid)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact file not found"
        )
    return SuccessRespose(detail="Your Contact File has been deleted")
