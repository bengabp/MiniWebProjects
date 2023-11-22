from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from enum import Enum

import os
from pathlib import Path
from datetime import datetime
from uuid import uuid4
import sqlite3

from favourites import favourites_router,Favourite
from helper_functions import get_dir_files

def create_database(path):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS favourites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT UNIQUE NOT NULL
    )
    """)

    cursor.close()
    connection.close()


BASE_DIR = Path(os.path.abspath(__file__))
FILES_UPLOAD_FOLDER = "server_files"

if not os.path.exists(FILES_UPLOAD_FOLDER):
    os.mkdir(FILES_UPLOAD_FOLDER)
    
DB_PATH = 'database.db'


create_database(DB_PATH)

app = FastAPI()
app.mount("/static",StaticFiles(directory='static'),name="static")
app.mount("/files",StaticFiles(directory= FILES_UPLOAD_FOLDER),name="files")

views_router = InferringRouter()
templates = Jinja2Templates(directory="templates")

FILE_TYPES = {
    "musics":['.mp3','.ogg','.wav'],
    "videos":['.mp4','.mk4','.mov'],
    "images":['.jpg','.png','.gif','.jpeg','.webm']
}

class ErrorCodes(Enum):
    UPLOADED_SUCCESSFULLY = 1
    FAILED_UPLOADING = -1


@cbv(views_router)
class MainAppView:
    @views_router.get("/",response_class=HTMLResponse)
    async def index(self,request:Request):
        return templates.TemplateResponse("index.html",{'request':request})


    @views_router.get("/get-all-files")
    async def get_all_files(self,request:Request,category:str=None,q=""):
        return {
                'message':'Got all files',
                'messageCode':1,
                'files':get_dir_files(FILES_UPLOAD_FOLDER,file_types=FILE_TYPES.get(category),search_query=q if len(q)>0 else None)
            }


    @views_router.post("/")
    async def upload_files(self,request:Request):
        file =  await request.form()
        file = file.get("file")

        try:
            filename = file.filename
            with open(f"{FILES_UPLOAD_FOLDER}/{filename}","wb") as uploading:
                uploading.write(file.file.read())
                
            return {
                'message':f'{filename} was uploaded',
                'messageCode':1
            }
        except AttributeError:
            return {
                    'message':f'{filename} is not a file',
                    'messageCode':-1,
                }

    @views_router.delete("/{filename}")
    async def delete_file(self,request:Request,filename:str):
        message = None
        messageCode = -1

        try:
            # Delete file from server 
            os.remove(f"{FILES_UPLOAD_FOLDER}/{filename}")

            # Delete file if its in favourites
            Favourite.delete_favourite_item(filename=filename)

            message = "File deleted"
            messageCode = 1

        except FileNotFoundError:
            message = "File not found"
            messageCode = -1

        return {
            "message":message,
            "messageCode":messageCode
        }

app.include_router(views_router)
app.include_router(favourites_router,prefix="/favourites")
