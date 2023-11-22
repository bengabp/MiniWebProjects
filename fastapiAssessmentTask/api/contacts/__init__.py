"""All of the helper funcitons that router module is using"""

from fastapi import UploadFile, Depends, HTTPException, status
from api.contacts.request_schemas import UserInDB
from api.contacts.response_schemas import (
    ContactFile,
    ContactSingleFile,
    ContactFileResponseList,
)
from api.contacts.schema import Contact
from api.config import (
    FAKE_USERS_DB,
    MONGO_DB_URL,
    MONGO_DB_DATABASE,
    OAUTH2_SCHEMA,
    CSV_FIELDS,
)
from typing import List, Annotated, Union, Tuple
from datetime import datetime
import pandas as pd
import pymongo
import uuid
import json


def is_valid_csv(file: UploadFile) -> Union[pd.DataFrame, bool]:
    """Validates the uploaded CSV file"""
    # Implement validation logic to check if the uploaded file is a valid CSV
    try:
        df = pd.read_csv(file.file)
        unique_columns = set(df.columns.to_list())
        needed_columns = set(CSV_FIELDS)
        if not needed_columns.issubset(
            unique_columns
        ):  # Check if user has uploaded a file which consist of all the needed columns.
            return False
        return df
    except pd.errors.EmptyDataError:
        return False
    except:
        return False
    

def parse_csv(df: pd.DataFrame) -> List[dict]:
    """Convert a pandas dataframe to json"""

    df = df[CSV_FIELDS]
    return df.to_json(orient="records")


def save_contacts_to_database(
    user_email: str, filename: str, contacts_data: List[dict]
):
    """Save Contact Data to our Underlying database"""

    contact_file_uuid = uuid.uuid4()
    contact_file_uuid_string = str(contact_file_uuid)

    client = pymongo.MongoClient(MONGO_DB_URL)
    db = client[MONGO_DB_DATABASE]
    # The user_contact_files collections stores all the contact_files uuid associated with a given user email
    users_contact_files = db["users_contact_files"]
    # The contact collections stores the actual content for all contacts associated with a given contact_files uuid
    contacts = db["contacts"]
    # If user is uploading for the first time, create a new document for him/her otherwise update his/her existing info with the new contact_file uid.
    user_email_query = {"_id": user_email}
    contact_file_uuid = {"$set": {contact_file_uuid_string: True}}
    users_contact_files.update_one(user_email_query, contact_file_uuid, upsert=True)
    current_datetime = datetime.now()
    # Insert the Contacts Info with revelant metadata for the given contact file.
    contacts.insert_one(
        {
            "_id": contact_file_uuid_string,
            "contact_info": contacts_data,
            "uploaded_date": datetime(
                current_datetime.year, current_datetime.month, current_datetime.day
            ),
            "filename": filename,
            "uploader": user_email,
        }
    )


def extract_dates(date_str: str) -> Tuple[Union[datetime, None], Union[datetime, None]]:
    """Extract date range from the given user string"""

    date_str = date_str.replace(" ", "")
    # Split the input string by the '-' character
    date_parts = date_str.split("-")
    if len(date_parts) == 1:
        try:
            end_date = datetime.strptime(date_parts[0], "%Y/%m/%d")
        except ValueError:
            return None, None
        return None, end_date
    # Parse the start date (first part of the split)
    try:
        start_date = datetime.strptime(date_parts[0], "%Y/%m/%d")
        end_date = datetime.strptime(date_parts[1], "%Y/%m/%d")
    except ValueError:
        return None, None

    return start_date, end_date


def get_contact_files_associated_with_users(
    user_email: str, date: Union[None, str]
) -> Union[ContactFileResponseList, bool]:
    """Get the Contact Files Information for a given user for the given date range"""
    client = pymongo.MongoClient(MONGO_DB_URL)
    db = client[MONGO_DB_DATABASE]
    users_contact_files = db["users_contact_files"]
    matching_contact_files = users_contact_files.find_one({"_id": user_email})
    if not matching_contact_files:
        return "No Contact Files"
    contacts = db["contacts"]
    contact_object_ids = [key for key in matching_contact_files if key != "_id"]
    print(contact_object_ids)
    if (
        date is None
    ):  # if not date-range is specified then return all the documents by the user
        query = {"_id": {"$in": contact_object_ids}}
    elif date is not None:
        start_date, end_date = extract_dates(date)  # extract the given date-range
        print(start_date, end_date)
        if start_date and end_date:  # if user has provided a range.
            query = {
                "$and": [
                    {"_id": {"$in": contact_object_ids}},
                    {"uploaded_date": {"$gte": start_date, "$lte": end_date}},
                ]
            }
        elif (
            end_date
        ):  # If only single date value is provided then only get the documents equal to user provided date
            query = {
                "$and": [
                    {"_id": {"$in": contact_object_ids}},
                    {"uploaded_date": end_date},
                ]
            }

        elif (
            start_date == None and end_date == None
        ):  # Not correct output. User has not provided the date in correct format
            return False
    matching_contact_documents = contacts.find(query)
    if not matching_contact_documents:
        return "No Contact Files"
    contact_file_list = []
    total_contacts_files = 0
    for contact in matching_contact_documents:
        contact_info = json.loads(contact["contact_info"])
        contact_file_list.append(
            ContactFile(
                uid=contact["_id"],
                uploadDate=contact["uploaded_date"].strftime("%Y/%m/%d"),
                totalContacts=len(contact_info),
            )
        )
        total_contacts_files += 1
    return ContactFileResponseList(
        contacts=contact_file_list, totalContacts=total_contacts_files
    )


def fetch_contact_by_uid(
    user_email: str, uid: Union[None, str]
) -> Union[bool, ContactSingleFile]:
    """Fetch a Specific Contact file for the given user-email"""
    client = pymongo.MongoClient(MONGO_DB_URL)
    db = client[MONGO_DB_DATABASE]
    contacts = db["contacts"]

    matching_contact_document = contacts.find_one({"_id": uid})
    if not matching_contact_document:
        return False
    contact_info = json.loads(matching_contact_document["contact_info"])

    if (
        matching_contact_document["uploader"] != user_email
    ):  # The contact file does not belong to the user
        return False
    elif matching_contact_document["uploader"] == user_email:
        return ContactSingleFile(
            uid=matching_contact_document["_id"],
            fileName=matching_contact_document["filename"],
            uploadDate=matching_contact_document["uploaded_date"].strftime("%Y/%m/%d"),
            totalContacts=len(contact_info),
        )


def get_csv_data(user_email: str, uid: str) -> Union[None, str]:
    """Get the CSV string data for the given contact uid file that has been uploaded"""
    client = pymongo.MongoClient(MONGO_DB_URL)
    db = client[MONGO_DB_DATABASE]
    contacts = db["contacts"]
    matching_contact_document = contacts.find_one({"_id": uid})
    if (
        not matching_contact_document
        or matching_contact_document["uploader"] != user_email
    ):  # The contact file does not belong to the user or the given contact file uid does not exists
        return False

    contact_info = json.loads(matching_contact_document["contact_info"])
    contact_info_df = pd.DataFrame(contact_info)

    return {
        "data": contact_info_df.to_csv(index=False),
        "name": matching_contact_document["filename"],
    }


def delete_validate_contact(user_email: str, uid: str) -> bool:
    """Delete the Contacts File from our db for the given uid. Also validates that contact file uid belongs to the user"""

    client = pymongo.MongoClient(MONGO_DB_URL)
    db = client[MONGO_DB_DATABASE]
    contacts = db["contacts"]
    users_contact_files = db["users_contact_files"]

    matching_contact_document = contacts.find_one({"_id": uid})
    if (
        not matching_contact_document
        or matching_contact_document["uploader"] != user_email
    ):  # The contact file does not belong to the user or the given contact file uid does not exists
        return False

    # Delete the contact file document
    contacts.delete_one({"_id": uid})
    # Delete the contact uid associated with the user
    update = {"$unset": {uid: ""}}
    users_contact_files.update_one({"_id": user_email}, update)
    return True


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):  ## This is just for dummy purposes
    user = get_user(FAKE_USERS_DB, token)
    return user


def fake_hash_password(password: str):  ## This is just for dummy purposes
    return "fakehashed" + password


def get_current_user(token: Annotated[str, Depends(OAUTH2_SCHEMA)]):
    """Get the current user and authenticates the user"""
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user
