from pydantic import BaseModel
from typing import List


#Advocates Base schema
class AdvocatesBase(BaseModel):

    id: int
    name: str
    profile_pic: str
    short_bio: str
    long_bio: str
    advocate_years_exp: int
    links: dict

#Advocates request schema for registring advocates
class AdvocatesRequest(BaseModel):
    short_bio: str
    long_bio: str
    advocate_years_exp: int
    links: dict

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
       company: CompanyResponse2