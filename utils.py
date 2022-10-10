import models
from auth import hash_password
from fastapi import status, HTTPException

def sign_up(email, password, company_name, request, db):
    email_check = db.query(models.Advocates).filter(models.Advocates.email == email).first()
    if email_check:
        raise HTTPException(status_code=406, detail=f'User with email -{email}- alredy exists!')
    password_hash = hash_password(password)
    company_id=db.query(models.Company.id).filter(models.Company.name == company_name)
    if not company_id.first():
        raise HTTPException(status_code=404, detail=f'Company with name -{company_name}- not found!')
    new_user = models.Advocates(
                                email=email, 
                                password=password_hash, 
                                company_id=company_id,
                                name=request.name, 
                                short_bio=request.short_bio, 
                                long_bio=request.long_bio, 
                                advocate_years_exp=request.advocate_years_exp
                                )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_advocates(db):
    return db.query(models.Advocates).all()

def get_advocates_id(id, db):
    user = db.query(models.Advocates).filter(models.Advocates.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f'User with id -{id}- not found!')
    return user

def new_company(name, href, request, db):
    company_check = db.query(models.Company).filter(models.Company.name == name).first()
    if company_check:
        raise HTTPException(status_code=406, detail=f'Company with name -{name}- alredy exists!')
    href = href.url.path
    new_company = models.Company(
                                name=name, 
                                logo=request.logo,
                                summary=request.summary, 
                                href=href)
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
        raise HTTPException(status_code=404, detail=f'Company with id -{id}- not found!')
    return company