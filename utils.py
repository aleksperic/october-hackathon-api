import io
import pathlib
import models
from uuid import uuid1
from auth import hash_password
from fastapi import HTTPException


BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / 'uploads'


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
    return destination

def sign_up(email, password, company_name, request, db):
    email_check = db.query(models.Advocates).filter(models.Advocates.email == email).first()
    if email_check:
        raise HTTPException(status_code=406, detail=f'User with email - {email} - alredy exists!')
    password_hash = hash_password(password)
    company_id=db.query(models.Company.id).filter(models.Company.name == company_name)
    if not company_id.first():
        raise HTTPException(status_code=404, detail=f'Company with name - {company_name} - not found! Register your company first.')

    new_user = models.Advocates(
                        email=email, 
                        password=password_hash, 
                        company_id=company_id,
                        name=request.name,
                        short_bio=request.short_bio, 
                        long_bio=request.long_bio, 
                        advocate_years_exp=request.advocate_years_exp,
                        ) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    for title, url in request.links.link:
        link_check = db.query(models.UserLinks).filter(models.UserLinks.url == url[1]).first()
        if link_check:
            db.delete(new_user)
            db.commit()
            raise HTTPException(status_code=406, detail=f'Url - {url[1]} - alredy exists in database!')
        new_link = models.UserLinks(title=title[1], url=url[1], user_id=new_user.id)
        db.add(new_link)

    db.commit()
    db.refresh(new_link)

    return new_user

def get_advocates(db):
    return db.query(models.Advocates).all()

def get_advocates_id(id, db):
    user = db.query(models.Advocates).filter(models.Advocates.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f'User with id - {id} - not found!')
    return user

def update_profile(request, current_user, db):
    user_obj = db.query(models.Advocates).filter(models.Advocates.email == current_user.email)
    to_update = {}
    for key, data in request:
        if not data:
            continue
        to_update[key] = data
    user_obj.update(to_update, synchronize_session=False)
    db.commit()
    return {'detail': 'Successfully updated!'}

def new_company(name, href, request, db):
    company_check = db.query(models.Company).filter(models.Company.name == name).first()
    if company_check:
        raise HTTPException(status_code=406, detail=f'Company with name - {name} - alredy exists!')
    href = href.url.path
    new_company = models.Company(
                        name=name,
                        summary=request.summary, 
                        href=href
                        )
    db.add(new_company)
    db.commit()
    new_company.href += f'/{new_company.id}'
    db.commit()
    db.refresh(new_company)
    return new_company
    
def get_companies(db):
    return db.query(models.Company).all()

def get_companies_id(id, db):
    company = db.query(models.Company).filter(models.Company.id == id).first()
    if not company:
        raise HTTPException(status_code=404, detail=f'Company with id - {id} - not found!')
    return company