from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class DocumentMetadata(BaseModel):
    file_name: Optional[str] = Field(..., description="Name of file")
    file_type: Optional[str] = Field(..., description="Type of file")
    pages: Optional[int] = Field(..., description="Number of pages")
    created: Optional[str] = Field(..., description="Date of file")
    size: Optional[int] = Field(..., description="Size of file")


class JsonFileSchema(BaseModel):
    user_email: Optional[EmailStr] = None
    filename: str
    type: str


__all__ = [
    "DocumentMetadata", "JsonFileSchema"
]
