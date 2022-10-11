from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
from typing import List
import schemas, utils


router = APIRouter()

@router.post('/companies', response_model=schemas.CompanyResponse2, tags=['Company'])
def new_company(
                name: str,
                href: Request,
                request: schemas.CompanyRequest, 
                db: Session = Depends(get_db),
                current_user: schemas.AdvocatesResponse = Depends(get_current_user)
                ):
    return utils.new_company(name, href, request, db)
    
@router.get('/companies', response_model=List[schemas.CompanyResponse1], tags=['Company'])
def get_companies(
                db: Session = Depends(get_db),
                current_user: schemas.AdvocatesResponse = Depends(get_current_user)
                ):
    return utils.get_companies(db)

@router.get('/companies/{id}', response_model=schemas.CompanyResponse1, tags=['Company'])
def get_companies_id(
                id: int,
                db: Session = Depends(get_db),
                current_user: schemas.AdvocatesResponse = Depends(get_current_user)
                ):
    return utils.get_companies_id(id, db)