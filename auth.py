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
SECRET_KEY = ''#env.str('SECRET_KEY')
ALGORITHM = 'H256'#env.str('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 60#env.int('ACCESS_TOKEN_EXPIRE_MINUTES')

router = APIRouter(
        prefix='',
        tags=['Authentifications']
        )

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )

# Custom login form
class OAuth2CustomForm:
    def __init__(self,  email: EmailStr = Form(), password: str = Form()):
        self.email = email
        self.password = password


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_from_db(id: int, db: Session):
    advocate = db.query(models.Advocates).filter(models.Advocates.id == id).first()
    if not advocate:
        return False
    return advocate

def authenticate_user(email: EmailStr, password: str, db: Session):
    advocate = db.query(models.Advocates).filter(models.Advocates.email == email).first()
    if advocate is None:
        raise CREDENTIALS_EXCEPTION
    if not verify_password(password, advocate.password):
        raise CREDENTIALS_EXCEPTION
    return advocate

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(expires_delta)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise CREDENTIALS_EXCEPTION
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = get_user_from_db(token_data.username, db)
    if not user:
        raise CREDENTIALS_EXCEPTION
    return user


@router.post('/login', response_model=schemas.Token)
def login_auth(form_data: OAuth2CustomForm = Depends(), db: Session = Depends(get_db)):
    print(form_data.email, form_data.password)
    user = authenticate_user(form_data.email, form_data.password, db)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    access_token = create_access_token({'sub': user.email}, ACCESS_TOKEN_EXPIRE_MINUTES)
    return {'access_token': access_token, 'token_type': 'bearer'}