from pydantic import BaseModel, EmailStr
from typing import List


#Advocates Base schema
class AdvocatesBase(BaseModel):

    id: int
    name: str
    password: str
    email: str
    profile_pic: str | None
    short_bio: str
    long_bio: str
    advocate_years_exp: int
    links: str | None
    class Config:
        orm_mode = True

#Advocates request schema for registring advocates
class AdvocatesRequest(BaseModel):
    
    name: str
    short_bio: str
    long_bio: str
    advocate_years_exp: int
    links: str

#Base information for company
class CompanyBase(BaseModel):
    id: int
    name: str
    logo: str | None

    class Config:
        orm_mode = True

#Extention from CompanyBase with more information for response to company routes
class CompanyResponse1(CompanyBase):
    summary: str
    advocates: List[AdvocatesBase] | None

#Extention from CompanyBase with href information for response to advocates routes
class CompanyResponse2(CompanyBase):
    href: str

class CompanyRequest(BaseModel):
    summary: str

#Advocates response schema for advocates routes
class AdvocatesResponse(AdvocatesBase):
       company: CompanyResponse2 | None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None