from fastapi import (
        APIRouter,
        Depends,
        Request,
        File,
        UploadFile, 
        )
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from typing import List
import schemas, utils


router = APIRouter(
            prefix='/companies',
            tags=['Company']
            )

@router.post('/', response_model=schemas.CompanyResponse, status_code=201)
def new_company(
            name: str,
            href: Request,
            request: schemas.CompanyRequest, 
            db: Session = Depends(get_db),
            #current_user: schemas.AdvocatesResponse = Depends(get_current_user)
            ):
    return utils.new_company(name, href, request, db)
    
@router.get('/', response_model=List[schemas.CompanyResponseAdvocates], status_code=200)
def get_companies(
            limit: int = 10,
            db: Session = Depends(get_db),
            ):
    return utils.get_companies(limit, db)

@router.get('/{id}/', response_model=schemas.CompanyResponseAdvocates, status_code=200)
def get_companies_id(
            id: int,
            db: Session = Depends(get_db),
            ):
    return utils.get_companies_id(id, db)

@router.put('/{id}/', response_model=schemas.CompanyResponse, status_code=202)
def update_summary(
            id: int, 
            request: schemas.CompanyUpdate,
        #     current_user: schemas.AdvocatesResponse = Depends(get_current_user),
            db: Session = Depends(get_db)
            ):
    return utils.update_summary(id, request,db)

@router.post('/upload_logo/{name}/', status_code=202)
async def upload_logo(
            name: str = Depends(schemas.CompanyPhotoUpload),
            file: UploadFile = File(...),
        #     current_user: schemas.AdvocatesResponse = Depends(get_current_user),
            db: Session = Depends(get_db)
            ):
    route = router.prefix
    return await utils.upload(file, name, db, route)