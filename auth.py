import models, schemas
from pydantic import EmailStr
from database import get_db
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from environs import Env
from jose import JWTError, jwt
from fastapi.param_functions import Form
from passlib.context import CryptContext
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


env = Env()
env.read_env()
SECRET_KEY = env.str('SECRET_KEY')
ALGORITHM = env.str('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = env.int('ACCESS_TOKEN_EXPIRE_MINUTES')

router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_from_db(email: EmailStr, db: Session):
    user = db.query(models.Advocates).filter(models.Advocates.email == email).first()
    if not user:
        return False
    return user

def authenticate_user(email: EmailStr, password: str, db: Session):
    user = db.query(models.Advocates).filter(models.Advocates.email == email).first()
    if user is None:
        raise CREDENTIALS_EXCEPTION
    if not verify_password(password, user.password):
        raise CREDENTIALS_EXCEPTION
    return user

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(expires_delta)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise CREDENTIALS_EXCEPTION
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = get_user_from_db(token_data.email, db)
    if not user:
        raise CREDENTIALS_EXCEPTION
    return user


@router.post('/login', response_model=schemas.Token, status_code=200, tags=['Signup/Login'])
def login_auth(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    access_token = create_access_token({'sub': user.email}, ACCESS_TOKEN_EXPIRE_MINUTES)
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.post('/sign_up', response_model=schemas.AdvocatesResponse, status_code=201, tags=['Signup/Login'])
def sign_up(
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
    
    for title, url in request.links.links:
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