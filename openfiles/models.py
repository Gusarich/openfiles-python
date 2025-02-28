"""
Data models for the Openfiles API.
"""

from typing import List, Optional, Union
from pydantic import BaseModel, Field


class BagResponse(BaseModel):
    """Response model for bag operations."""

    bag_id: str


class ValidationError(BaseModel):
    """Validation error model."""

    loc: List[Union[str, int]] = Field(..., title="Location")
    msg: str = Field(..., title="Message")
    type: str = Field(..., title="Error Type")


class HTTPValidationError(BaseModel):
    """HTTP validation error model."""

    detail: Optional[List[ValidationError]] = Field(None, title="Detail")


class FileInfoResponse(BaseModel):
    """File information response model."""

    filename: str
    size: int
    uploaded_at: float
    description: str
    bag_id: str


class UserResponse(BaseModel):
    """User information response model."""

    uid: str
    space_left: float
    capacity: float
