import io
import pathlib
import models
from uuid import uuid1
from fastapi import HTTPException


BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / 'uploads'


# Function for uploading photos/logos for advocates/companies

async def upload(file, user, db, route):

    uploaded_file = await file.read()

    file_name = pathlib.Path(file.filename)
    file_ext = file_name.suffix.lower()

    if len(uploaded_file) > 2_000_000:
        raise HTTPException(status_code=413, detail='Uploaded file should be less than 2MB')
    if file_ext not in ['.jpg', '.jpeg', '.png']:
        raise HTTPException(status_code=422, detail='Only JPG/JPEG/PNG format supported!')
    
    bytes_str = io.BytesIO(uploaded_file)
    
    if route == '/advocates':
        destination = UPLOAD_DIR / f'advocates/{uuid1()}{file_ext}'
        with open(str(destination), 'wb') as out:
            out.write(bytes_str.read())
        user = db.query(models.Advocates).filter(models.Advocates.name == user.name)
        user.update({'profile_pic': str(destination)})
    
    if route == '/companies':
        destination = UPLOAD_DIR / f'companies/{uuid1()}{file_ext}'
        with open(str(destination), 'wb') as out:
            out.write(bytes_str.read())
        company = db.query(models.Company).filter(models.Company.name == user.name)
        company.update({'logo': str(destination)})

    db.commit()
    return {'path_to_file': destination}

# Advocates routes

def get_advocates(db):
    return db.query(models.Advocates).all()

def get_advocates_id(id, db):
    user = db.query(models.Advocates).filter(models.Advocates.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f'User with id - {id} - not found!')
    return user

def my_profile(current_user):
    return current_user

def update_profile(request, current_user, db):
    user_obj = db.query(models.Advocates).filter(models.Advocates.email == current_user.email)
    to_update = {}
    for key, data in request:
        if not data:
            continue
        to_update[key] = data
    user_obj.update(to_update, synchronize_session=False)
    db.commit()
    return user_obj.first()

def update_links(request, current_user, db):
    links_obj = db.query(models.UserLinks).filter(models.UserLinks.user_id == current_user.id)
    links_obj_titles = [link.title for link in links_obj]

    for link in request.links:
        if not(link.title in links_obj_titles):
            new_link = models.UserLinks(title=link.title, url=link.url, user_id=current_user.id)
            db.add(new_link)

        link_to_update = db.query(models.UserLinks).filter(models.UserLinks.title == link.title)
        link_to_update.update({'title': link.title, 'url': link.url}, synchronize_session=False)
    db.commit()
    
    return list(links_obj)

def delete_advocate(current_user, db):
    links = db.query(models.UserLinks).filter(models.UserLinks.user_id == current_user.id)
    links.delete(synchronize_session=False)
    user = db.query(models.Advocates).filter(models.Advocates.id == current_user.id)
    user.delete(synchronize_session=False)
    db.commit()

    return {'detail': 'Deleted!'}


# Companies routes

def new_company(name, href, request, db):
    company_check = db.query(models.Company).filter(models.Company.name == name).first()
    if company_check:
        raise HTTPException(status_code=406, detail=f'Company with name - {name} - alredy exists!')
        
    href = href.url.path
    new_company = models.Company(name=name, summary=request.summary, href=href)
    db.add(new_company)
    db.commit()
    new_company.href += f'/{new_company.id}'
    db.commit()
    db.refresh(new_company)
    return new_company
    
def get_companies(db):
    return db.query(models.Company).all()

def update_summary(id, request, db):
    company = db.query(models.Company).filter(models.Company.id == id)
    if not company.first():
        raise HTTPException(status_code=404, detail=f'Company with id - {id} - not found!')
    company.update({'summary': request.summary}, synchronize_session=False)
    db.commit()

    return company.first()

def get_companies_id(id, db):
    company = db.query(models.Company).filter(models.Company.id == id).first()
    if not company:
        raise HTTPException(status_code=404, detail=f'Company with id - {id} - not found!')
    return company