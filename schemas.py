from typing import List, Dict, Optional
from pydantic import BaseModel, EmailStr, Field


# Advocates base schema
class AdvocatesBase(BaseModel):

    id: int
    name: str
    password: str
    email: EmailStr
    profile_pic: str | None = None
    short_bio: str
    long_bio: str
    advocate_years_exp: int
    links: Dict[str, str] | None = None
    class Config:
        orm_mode = True

# Advocates request schema for registring advocates
class AdvocatesRequest(BaseModel):
    
    name: str
    short_bio: str
    long_bio: str
    advocate_years_exp: int
    links: Dict[str, str] | None = None

# Advocates request schema for updating Advocates
class AdvocatesUpdateRequest(AdvocatesRequest):
    password: str | None

# Company base schema
class CompanyBase(BaseModel):
    id: int
    name: str
    logo: str | None = None

    class Config:
        orm_mode = True

# Extention from CompanyBase with more information for response to company routes
class CompanyResponse1(CompanyBase):
    summary: str
    advocates: List[AdvocatesBase] | None

# Extention from CompanyBase with href information for response to advocates routes
class CompanyResponse2(CompanyBase):
    href: str

# Company request schema
class CompanyRequest(BaseModel):
    summary: str | None

# Company schema for uploading photos
class CompanyPhotoUpload(BaseModel):
    name: str

#A dvocates response schema for advocates routes
class AdvocatesResponse(AdvocatesBase):
       company: CompanyResponse2 | None

# Token response schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Token data schema
class TokenData(BaseModel):
    email: EmailStr | None = None