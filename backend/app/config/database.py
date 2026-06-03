from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if not MONGO_URI or not DATABASE_NAME:
    raise RuntimeError(
        "MONGO_URI e DATABASE_NAME devem estar definidos como variáveis de ambiente"
    )

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=20000,
    connectTimeoutMS=20000,
)

db = client[DATABASE_NAME]