import auth, advocates, company, utils
from database import Base, engine, get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware


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

# Search route

@app.get('/search')
def search(
        query: str = Query(default=None), 
        db: Session = Depends(get_db)
        ):
    return utils.search(query, db)