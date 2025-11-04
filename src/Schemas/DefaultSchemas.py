from typing import Optional

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    file_name: Optional[str] = Field(..., description="Name of file")
    file_type: Optional[str] = Field(..., description="Type of file")
    pages: Optional[int] = Field(..., description="Number of pages")
    created: Optional[str] = Field(..., description="Date of file")
    size: Optional[int] = Field(..., description="Size of file")


__all__ = [
    "DocumentMetadata",
]
