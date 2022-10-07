from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Advocates(Base):

    __tablename__ = 'advocates'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    password = Column(String)
    email = Column(String)
    profile_pic = Column(String)
    short_bio = Column(String)
    long_bio = Column(String)
    advocate_years_exp = Colunm(Integer)
    links = Column(String)

    company = relationship('Company', back_populates='advocates')

class Company(Base):

    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    logo = Column(String)
    summary = Column(String)
    href = Column(String)
    advocates_id = Column(Integer, ForeignKey('advocates.id'))

    advocates = relationship('Advocates', back_populates='company')