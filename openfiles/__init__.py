"""
Openfiles Python SDK
~~~~~~~~~~~~~~~~~~~

A Python SDK for interacting with the Openfiles API.

The SDK supports authentication via API token provided directly or 
through the OPENFILES_API_TOKEN environment variable.

:copyright: (c) 2023 Openfiles
:license: MIT, see LICENSE for more details.
"""

from .client import OpenfilesClient
from .models import (
    BagResponse,
    FileInfoResponse,
    UserResponse,
    HTTPValidationError,
    ValidationError,
)

__all__ = [
    "OpenfilesClient",
    "BagResponse",
    "FileInfoResponse",
    "UserResponse",
    "HTTPValidationError",
    "ValidationError",
]

__version__ = "0.1.0"
