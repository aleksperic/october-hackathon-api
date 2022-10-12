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

@router.post('', response_model=schemas.CompanyResponse2)
def new_company(
            name: str,
            href: Request,
            request: schemas.CompanyRequest, 
            db: Session = Depends(get_db),
            #current_user: schemas.AdvocatesResponse = Depends(get_current_user)
            ):
    return utils.new_company(name, href, request, db)
    
@router.get('', response_model=List[schemas.CompanyResponse1])
def get_companies(
            db: Session = Depends(get_db),
            current_user: schemas.AdvocatesResponse = Depends(get_current_user)
            ):
    return utils.get_companies(db)

@router.get('/{id}', response_model=schemas.CompanyResponse1)
def get_companies_id(
            id: int,
            db: Session = Depends(get_db),
            current_user: schemas.AdvocatesResponse = Depends(get_current_user)
            ):
    return utils.get_companies_id(id, db)

@router.post('/upload/{name}')
async def upload_photo(
            name: str = Depends(schemas.CompanyPhotoUpload),
            file: UploadFile = File(...),
            db: Session = Depends(get_db)
            ):
    route = router.prefix
    return await utils.upload(file, name, db, route)