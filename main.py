import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
import motor.motor_asyncio
from services.config import MONGO_URI, DB_NAME

# ייבוא כל המודלים
from models.event import Event
from models.customer import Customer
from models.Category import Category
from models.categories_of_event import CategoryOfEvent

# ייבוא כל ה-routers
from controllers.event_controller import router as event_router
from controllers.customer_controller import router as customer_router
from controllers.category_controller import router as category_router
from controllers.category_of_event_controller import router as category_of_event_router

app = FastAPI(title="PicUp API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# הוספת כל ה-routers
app.include_router(event_router)
app.include_router(customer_router)
app.include_router(category_router)
app.include_router(category_of_event_router)

# אתחול MongoDB + Beanie
async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    await init_beanie(database=db, document_models=[
        Event,
        Customer,
        Category,
        CategoryOfEvent
    ])

@app.on_event("startup")
async def startup():
    await init_db()
