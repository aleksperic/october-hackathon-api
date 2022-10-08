from fastapi import FastAPI, UploadFile, File, Query
from pydantic import EmailStr
import schemas, auth

app = FastAPI()

app.include_router(auth.router)

@app.get('/')
def index():
    return {'hello': 'world'}


@app.post('/upload_photo', tags=['admin'])
async def upload_photo(file: bytes = File()):
    # print(file.content_type)
    return file

#Advocates routes

@app.post('/advocates', response_model=schemas.AdvocatesResponse, tags=['Advocates'])
def set_advocates(
                email: str,
                password: str,
                request: schemas.AdvocatesRequest):

    return data

@app.get('/advocates', tags=['Advocates'])
def get_advocates():
    return data

@app.get('/advocates/{id}', tags=['Advocates'])
def get_advocates_id():
    pass

#Companies routes

@app.post('/companies', tags=['Company'])
def set_companies():
    pass

@app.get('/companies/', tags=['Company'])
def get_companies():
    pass

@app.get('/companies/{id}', tags=['Company'])
def get_companies_id():
    pass