from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from typing import List
import schemas, utils


router = APIRouter(
            prefix='/advocates',
            tags=['Advocates']
            )

#Advocates routes
@router.post('/sign_up', response_model=schemas.AdvocatesResponse, tags=['Signup/Login'])
def sign_up(
            email: str,
            password: str,
            company_name: str,
            request: schemas.AdvocatesRequest,
            db: Session = Depends(get_db)
            ):
    return utils.sign_up(email, password, company_name, request, db)

@router.get('/', response_model=List[schemas.AdvocatesResponse])
def get_advocates(
                current_user: schemas.AdvocatesResponse = Depends(get_current_user), 
                db: Session = Depends(get_db)
                ):
    return utils.get_advocates(db)

@router.get('/{id}', response_model=schemas.AdvocatesResponse)
def get_advocates_id(
                    id: int, 
                    db: Session = Depends(get_db),
                    current_user: schemas.AdvocatesResponse = Depends(get_current_user)
                    ):
    return utils.get_advocates_id(id, db)

@router.get('/me/profile', response_model=schemas.AdvocatesResponse)
def my_profile(current_user: schemas.AdvocatesResponse = Depends(get_current_user)):
    return current_user

@router.post('/upload')
async def upload_photo(
                file: UploadFile = File(...),
                current_user: schemas.AdvocatesResponse = Depends(get_current_user), 
                db: Session = Depends(get_db)
                ):
  
    return await utils.upload(file, current_user, db)