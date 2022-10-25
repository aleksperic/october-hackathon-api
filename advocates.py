from fastapi import (
            APIRouter,
            Depends,
            File,
            UploadFile
            )
from pydantic import EmailStr
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user, hash_password
from typing import List
import schemas, utils, models


router = APIRouter(
            prefix='/advocates',
            tags=['Advocates']
            )

# Advocates routes

@router.post('/', response_model=schemas.AdvocatesResponse, status_code=201)
def new_advocate(
            email: EmailStr,
            password: str,
            request: schemas.AdvocatesRequest,
            db: Session = Depends(get_db)
            ):
    
    email_check = db.query(models.Advocates).filter(models.Advocates.email == email).first()
    if email_check:
        raise HTTPException(status_code=406, detail=f'User with email - {email} - alredy exists!')

    password_hash = hash_password(password)

    company_id = db.query(models.Company.id).filter(models.Company.name == request.company_name)
    if not company_id.first():
        company_id = None

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
    
    for title, url in request.links:
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

@router.get('/', response_model=List[schemas.AdvocatesResponse], status_code=200)
def get_advocates(
            limit: int = 10,
            db: Session = Depends(get_db)
            ):
    return utils.get_advocates(limit, db)

@router.get('/{id}/', response_model=schemas.AdvocatesResponse, status_code=200)
def get_advocates_id(
            id: int, 
            db: Session = Depends(get_db)
            ):
    return utils.get_advocates_id(id, db)

@router.get('/me/profile/', response_model=schemas.AdvocatesResponse, status_code=200)
def my_profile(
            current_user: schemas.AdvocatesResponse = Depends(get_current_user)
            ):
    return utils.my_profile(current_user)

@router.put('/me/update/', response_model=schemas.AdvocatesResponse, status_code=202)
def update_profile(
            request: schemas.AdvocatesUpdateRequest,
            current_user: schemas.AdvocatesResponse = Depends(get_current_user), 
            db: Session = Depends(get_db)
            ):
    return utils.update_profile(request, current_user, db)

@router.put('/me/update_links/', response_model=List[schemas.UserLinksResponse], status_code=202)
def update_links(
            request: schemas.UserLinksRequest,
            current_user: schemas.AdvocatesResponse = Depends(get_current_user),
            db: Session = Depends(get_db)
            ):
    return utils.update_links(request, current_user, db)

@router.post('/me/upload_photo/', status_code=202)
async def upload_photo(
            file: UploadFile = File(...),
            current_user: schemas.AdvocatesResponse = Depends(get_current_user), 
            db: Session = Depends(get_db)
            ):
    route = router.prefix
    return await utils.upload(file, current_user, db, route)

@router.delete('/me/delete/', status_code=200)
def delete_advocate(
            current_user:  schemas.AdvocatesResponse = Depends(get_current_user), 
            db: Session = Depends(get_db)
            ):
    return utils.delete_advocate(current_user, db)