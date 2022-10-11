from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import schemas, auth, models, advocates, company


app = FastAPI()

Base.metadata.create_all(engine)

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth.router)
app.include_router(advocates.router)
app.include_router(company.router)