from fastapi import FastAPI, Request
from database import Base, engine
import schemas, auth, models, advocates, company


app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(advocates.router)
app.include_router(company.router)