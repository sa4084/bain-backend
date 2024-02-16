# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
    allow_headers=["*"], 
)

# SQLite database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./weather.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define models
class PastWeather(Base):
    __tablename__ = "past_weather"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_downloading = Column(Boolean)

class CurrentWeather(Base):
    __tablename__ = "current_weather"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class PastWeatherRequest(BaseModel):
    query: str
    startDate: datetime
    endDate: datetime
    isDownloading: bool

class CurrentWeatherRequest(BaseModel):
    query: str

@app.post("/pastWeather")
async def fetch_past_weather(data: PastWeatherRequest):
    db = SessionLocal()
    db_past_weather = PastWeather(
        query=data.query,
        start_date=data.startDate,
        end_date=data.endDate,
        is_downloading=data.isDownloading
    )
    db.add(db_past_weather)
    db.commit()
    db.refresh(db_past_weather)
    db.close()
    return {"message": "Past weather data stored successfully"}

@app.post("/currentWeather")
async def fetch_current_weather(data: CurrentWeatherRequest):
    print(data.query,'---')
    db = SessionLocal()
    db_current_weather = CurrentWeather(query=data.query)
    print(db_current_weather)
    db.add(db_current_weather)
    db.commit()
    db.refresh(db_current_weather)
    db.close()
    return {"message": "Current weather data stored successfully"}
