from typing import List, Dict, Optional
from pydantic import BaseModel, EmailStr, Field

class UserLinks(BaseModel):
    id: int
    title: str
    url: str
    user_id: int

class UserLinksResponse(BaseModel):
    title: str
    url: str
    class Config:
        orm_mode=True

class UserLinksRequest(BaseModel):
    title: str
    url: str
    class Config:
        orm_mode=True

# Advocates base schema
class AdvocatesBase(BaseModel):

    id: int
    name: str 
    email: EmailStr
    profile_pic: str | None = None
    short_bio: str
    long_bio: str
    advocate_years_exp: int
    links: List[UserLinksResponse] | None = None
    class Config:
        orm_mode = True

# Advocates request schema for registring advocates
class AdvocatesRequest(BaseModel):
    
    name: str | None = Field(default=None, title="Full name", max_length=50)
    company_name: str | None = Field(default=None, title="Company name", max_length=50)
    short_bio: str | None = Field(default=None, title="Short bio", max_length=100)
    long_bio: str | None = Field(default=None, title="Long bio", max_length=300)
    advocate_years_exp: int | None = Field(ge=0, default=None, title="Years of experience")
    links: List[UserLinksRequest] | None

# Advocates request schema for updating Advocates
class AdvocatesUpdateRequest(BaseModel):
    name: str | None = None
    company_name: str | None = None
    short_bio: str | None = None
    long_bio: str | None = None
    advocate_years_exp: int | None = None

# Company base schema
class CompanyBase(BaseModel):
    id: int
    name: str
    logo: str | None = None
    summary: str

    class Config:
        orm_mode = True

# Extention from CompanyBase with more information for response to company routes
class CompanyResponseAdvocates(CompanyBase):
    summary: str
    advocates: List[AdvocatesBase] | None

# Extention from CompanyBase with href information for response to advocates routes
class CompanyResponse(CompanyBase):
    href: str

# Company request schema
class CompanyRequest(BaseModel):
    summary: str | None = Field(default=None, title="The summary of the company", max_length=300)

# Company schema for uploading photos
class CompanyPhotoUpload(BaseModel):
    name: str

# Advocates response schema for advocates routes
class AdvocatesResponse(AdvocatesBase):
       company: CompanyResponse | None

# Company summary update schema
class CompanyUpdate(CompanyRequest):
    pass

# Token response schema
class Token(BaseModel):
    access_token: str
    token_type: str

# Token data schema
class TokenData(BaseModel):
    email: EmailStr | None = None