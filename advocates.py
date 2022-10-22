from fastapi import (
            APIRouter,
            Depends,
            File,
            UploadFile
            )
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from typing import List
import schemas, utils


router = APIRouter(
            prefix='/advocates',
            tags=['Advocates']
            )

# Advocates routes

@router.get('', response_model=List[schemas.AdvocatesResponse], status_code=200)
def get_advocates(
            db: Session = Depends(get_db)
            ):
    return utils.get_advocates(db)

@router.get('/{id}', response_model=schemas.AdvocatesResponse, status_code=200)
def get_advocates_id(
            id: int, 
            db: Session = Depends(get_db)
            ):
    return utils.get_advocates_id(id, db)

@router.get('/me/profile', response_model=schemas.AdvocatesResponse, status_code=200)
def my_profile(
            current_user: schemas.AdvocatesResponse = Depends(get_current_user)
            ):
    return utils.my_profile(current_user)

@router.put('/me/update', status_code=202)
def update_profile(
            request: schemas.AdvocatesUpdateRequest,
            current_user: schemas.AdvocatesResponse = Depends(get_current_user), 
            db: Session = Depends(get_db)
            ):
    return utils.update_profile(request, current_user, db)

@router.put('/me/update_links', response_model=List[schemas.UserLinksResponse], status_code=202)
def update_links(
            request: schemas.UserLinksRequest,
            current_user: schemas.AdvocatesResponse = Depends(get_current_user),
            db: Session = Depends(get_db)
            ):
    return utils.update_links(request, current_user, db)

@router.post('/me/upload_photo', status_code=202)
async def upload_photo(
            file: UploadFile = File(...),
            current_user: schemas.AdvocatesResponse = Depends(get_current_user), 
            db: Session = Depends(get_db)
            ):
    route = router.prefix
    return await utils.upload(file, current_user, db, route)

@router.delete('/me/delete', status_code=200)
def delete_advocate(
            current_user:  schemas.AdvocatesResponse = Depends(get_current_user), 
            db: Session = Depends(get_db)
            ):
    return utils.delete_advocate(current_user, db)