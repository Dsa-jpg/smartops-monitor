from fastapi import FastAPI
from app.routers import users, auth
from app.db import Base, engine


#Base.metadata.create_all(bind=engine)

app = FastAPI()



app.include_router(users.router)
app.include_router(auth.router)