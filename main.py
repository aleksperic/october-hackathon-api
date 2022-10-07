from fastapi import FastAPI, UploadFile
import schemas

app = FastAPI()


@app.get('/')
def index():
    return {'hello': 'world'}

#Advocates routes

@app.post('/advocates', response_model=schemas.AdvocatesResponse)
def set_advocates(
                name: str, 
                profile_pic: UploadFile,
                request: schemas.AdvocatesRequest):
    return request

@app.get('/advocates')
def get_advocates():
    pass

@app.get('/advocates/{id}')
def get_advocates_id():
    pass

#Companies routes

@app.post('/companies')
def set_companies():
    pass

@app.get('/companies/')
def get_companies():
    pass

@app.get('/companies/{id}')
def get_companies_id():
    pass