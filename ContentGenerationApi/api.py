from fastapi import FastAPI,Request
from titlecontent import generate_text_title

api = FastAPI()

@api.get("/generate-text-title")
def generate_text_title_handler(request:Request,text:str):
    return {
        'status':'succes',
        'text':text,
        'title':generate_text_title(text)
    }