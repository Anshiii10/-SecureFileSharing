from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    username: str
    email: str
    hashed_password: str
    role: str  # "ops" or "client"
    is_active: bool = True

class FileMetadata(BaseModel):
    id: Optional[str]
    filename: str
    content_type: str
    uploader_id: str
    download_url: Optional[str]
    encrypted: bool = False
