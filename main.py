from fastapi import FastAPI, UploadFile, File
import schemas

app = FastAPI()


@app.get('/')
def index():
    return {'hello': 'world'}


@app.post('/upload_photo')
async def upload_photo(file: bytes = File()):
    # print(file.content_type)
    return file

#Advocates routes

@app.post('/advocates', response_model=schemas.AdvocatesResponse)
def set_advocates(
    id: int,
                name: str, 
                profile_pic: str,
                request: schemas.AdvocatesRequest):

    data={'id': id, 'name': name, 'profile_pic': profile_pic, 'short_bio': request.short_bio, 'long_bio': request.long_bio, 'advocate_years_exp': request.advocate_years_exp, 'links': request.links}
    print(data)
    return data

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