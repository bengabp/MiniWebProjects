from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from pydantic import BaseModel

import sqlite3

from helper_functions import get_dir_files

favourites_router = InferringRouter()

class FavItem(BaseModel):
    filename:str

@cbv(favourites_router)
class Favourite:
    def __init__(self):
        pass

    @favourites_router.get("/")
    def get_favourites(self):
        message = "Error fetching favourite files"
        messageCode = -1

        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM favourites")
            results = cursor.fetchall()
            message = "Favourite Items"
            messageCode = 1

            results = [get_dir_files(f"server_files/{res[1]}",is_file=True) for res in results if get_dir_files(f"server_files/{res[1]}",is_file=True) is not None]

        return {
            "message":message,
            "messageCode":messageCode,
            "results":results
        }


    @favourites_router.post("/")
    def new_favourite(self,favitem:FavItem):
        message = "Error"
        messageCode = -1

        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            try:
                file_details = get_dir_files(f"server_files/{favitem.filename}",is_file=True)
                if file_details is None:raise FileNotFoundError("File does not exists !")
                cursor.execute("INSERT INTO favourites (filename) VALUES (?)",(favitem.filename,))
                message = "Favourite Item saved"
                messageCode = 1
            except sqlite3.IntegrityError:
                message = "Error, Item is already in favourites"
                messageCode = -1
            except FileNotFoundError:
                message = "Error, File does not exist"
                messageCode = -1

        return {
            "message":message,
            "messageCode":messageCode
        }

    @favourites_router.delete("/{filename}")
    def delete_favourite(self,filename:str):
        message = "Error"
        messageCode = -1

        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM favourites WHERE filename=?",(filename,))
                message = "Favourite Item Deleted"
                messageCode = 1
            except sqlite3.IntegrityError:
                message = "Error deleting item"
                messageCode = -1

        return {
            "message":message,
            "messageCode":messageCode
        }

    @classmethod
    def delete_favourite_item(cls,filename):
        message = "Error"
        messageCode = -1

        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM favourites WHERE filename=?",(filename,))
                message = "Favourite Item Deleted"
                messageCode = 1
            except sqlite3.IntegrityError:
                message = "Error deleting item"
                messageCode = -1

        return {
            "message":message,
            "messageCode":messageCode
        }