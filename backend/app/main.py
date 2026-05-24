from fastapi import FastAPI
from app.config.database import db
from app.routes.books import router as books_router
from app.routes.students import router as students_router
from app.routes.loans import router as loans_router

app = FastAPI()
app.include_router(books_router)
app.include_router(students_router)
app.include_router(loans_router)


@app.get("/")
def home():
    db.command("ping")

    return {
        "message": "MongoDB Atlas conectado"
    }