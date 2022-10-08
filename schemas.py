from pydantic import BaseModel, EmailStr
from typing import List, Dict


#Advocates Base schema
class AdvocatesBase(BaseModel):

    id: int
    name: str
    password: str
    email: EmailStr
    profile_pic: str
    short_bio: str
    long_bio: str
    advocate_years_exp: int
    links: Dict | None

#Advocates request schema for registring advocates
class AdvocatesRequest(BaseModel):
    password: str
    email: EmailStr
    short_bio: str
    long_bio: str
    advocate_years_exp: int
    links: Dict | None

#Base information for company
class CompanyBase(BaseModel):
    id: int
    name: str
    logo: str

#Extention from CompanyBase with more information for response to company routes
class CompanyResponse1(CompanyBase):
    summary: str
    advocates: List[AdvocatesBase]

#Extention from CompanyBase with href information for response to advocates routes
class CompanyResponse2(CompanyBase):
    href: str

#Advocates response schema for advocates routes
class AdvocatesResponse(AdvocatesBase):
       company: CompanyResponse2 | None

class Token(BaseModel):
    access_token: str
    token_type: str
