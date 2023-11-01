from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import userModel
from database.database import engine
from routes import jobSeekerRoutes, companyRoutes, advertisementRoutes, jobApplicationRoutes

app = FastAPI()

userModel.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobSeekerRoutes.router)
app.include_router(companyRoutes.router)
app.include_router(advertisementRoutes.router)
app.include_router(jobApplicationRoutes.router)