from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class Advocates(Base):

    __tablename__ = 'advocates'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    profile_pic = Column(String)
    short_bio = Column(String)
    long_bio = Column(String)
    advocate_years_exp = Column(Integer)
    company_id = Column(Integer, ForeignKey('company.id'))

    company = relationship('Company', back_populates='advocates')
    links = relationship('UserLinks', back_populates='advocates', cascade="delete", passive_deletes=True)

class Company(Base):

    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    logo = Column(String)
    summary = Column(String)
    href = Column(String)

    advocates = relationship('Advocates', back_populates='company')

class UserLinks(Base):
    
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey('advocates.id', ondelete='CASCADE'))

    advocates = relationship('Advocates', back_populates='links')