import uvicorn
from fastapi import FastAPI
from api.api_v1.endpoints.instructors import instructors
from api.api_v1.endpoints.learners import learners
from api.db.database import database

app = FastAPI()

app.include_router(instructors, prefix='/api/v1/instructors', tags=["Instructors"])
app.include_router(learners, prefix='/api/v1/learners', tags=["Learners"])

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
