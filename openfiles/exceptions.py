from typing import Any, Dict
from openfiles.models import HTTPValidationError


class OpenfilesError(Exception):
    """Base exception for all Openfiles API errors."""

    pass


class OpenfilesValidationError(OpenfilesError):
    """Exception raised when API validation fails."""

    def __init__(self, validation_error: HTTPValidationError):
        self.validation_error = validation_error
        self.details = validation_error.detail
        message = self._format_message()
        super().__init__(message)

    def _format_message(self) -> str:
        """Format validation errors for better readability."""
        if not self.details:
            return "Unknown validation error"

        errors = []
        for error in self.details:
            location = " -> ".join(str(loc) for loc in error.loc)
            errors.append(f"{location}: {error.msg} ({error.type})")

        return "\n".join(errors)


class OpenfilesAPIError(OpenfilesError):
    """Exception raised for API errors with a JSON response."""

    def __init__(self, status_code: int, error_data: Dict[str, Any]):
        self.status_code = status_code
        self.error_data = error_data
        message = f"API Error ({status_code}): {error_data}"
        super().__init__(message)


class OpenfilesHTTPError(OpenfilesError):
    """Exception raised for general HTTP errors."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"HTTP Error ({status_code}): {message}")
