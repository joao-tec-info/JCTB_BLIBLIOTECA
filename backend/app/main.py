from fastapi import FastAPI
from app.config.database import db


app = FastAPI()


@app.get("/")
def home():

    db.command("ping")

    return {
        "message": "MongoDB Atlas conectado"
    }