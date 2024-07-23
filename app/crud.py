from pymongo import MongoClient
from bson import ObjectId
from passlib.context import CryptContext
from .models import User, FileMetadata
from .config import settings

client = MongoClient(settings.mongodb_url)
db = client.file_sharing

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(username: str):
    return db.users.find_one({"username": username})

def create_user(user: User):
    user.hashed_password = pwd_context.hash(user.hashed_password)
    db.users.insert_one(user.dict())

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if user and pwd_context.verify(password, user["hashed_password"]):
        return user
    return False

def create_file_metadata(file_meta: FileMetadata):
    db.files.insert_one(file_meta.dict())
