from fastapi import FastAPI
from app.routers import users, auth, services, alerts
from app.db import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()



app.include_router(users.router)
app.include_router(auth.router)
app.include_router(services.router)
app.include_router(alerts.router)