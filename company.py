from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import schemas, utils


router = APIRouter()

@router.post('/companies', response_model=schemas.CompanyBase, tags=['Company'])
def new_company(
                request: schemas.CompanyRequest, 
                db: Session = Depends(get_db)
                ):
    return utils.new_company(request, db)
    
@router.get('/companies/', response_model=schemas.CompanyResponse1, tags=['Company'])
def get_companies(
                db: Session = Depends(get_db)
                ):
    return utils.get_companies(db)

@router.get('/companies/{id}', response_model=schemas.CompanyResponse1, tags=['Company'])
def get_companies_id(
                id: int,
                db: Session = Depends(get_db),
                ):
    return utils.get_companies_id(id, db)