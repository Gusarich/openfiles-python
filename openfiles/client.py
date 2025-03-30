"""
Openfiles API Client
"""

import os
import requests
from typing import List, Optional, Dict, Any, Union
from pathlib import Path

from openfiles.exceptions import (
    OpenfilesAPIError,
    OpenfilesHTTPError,
    OpenfilesValidationError,
)

from .models import BagResponse, FileInfoResponse, UserResponse, HTTPValidationError


class OpenfilesClient:
    """
    Client for interacting with the Openfiles API.
    """

    BASE_URL = "https://app.openfiles.xyz"  # Default base URL

    def __init__(self, api_token: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the Openfiles client.

        Args:
            api_token: API token for authentication. If not provided,
                       will try to get it from OPENFILES_API_TOKEN env var.
            base_url: Optional custom base URL for the API
        """
        self.api_token = api_token or os.environ.get("OPENFILES_API_TOKEN")
        if not self.api_token:
            raise ValueError(
                "API token must be provided either as a parameter or "
                "through the OPENFILES_API_TOKEN environment variable"
            )
        self.base_url = base_url or self.BASE_URL

    def _get_headers(self) -> Dict[str, str]:
        """
        Get the headers for API requests.

        Returns:
            Dict with authorization headers
        """
        return {"X-Authorization": self.api_token}

    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handle the API response.

        Args:
            response: Response object from requests

        Returns:
            Parsed response data

        Raises:
            OpenfilesValidationError: For validation errors
            OpenfilesAPIError: For API errors with JSON response
            OpenfilesHTTPError: For other HTTP errors
        """
        # Check if the response indicates an error
        if not response.ok:
            try:
                error_data = response.json()

                # If response contains validation error structure
                if "detail" in error_data:
                    # Check if detail is a string (simple error message)
                    if isinstance(error_data["detail"], str):
                        # Simple error message
                        raise OpenfilesAPIError(response.status_code, error_data)
                    # Otherwise try to parse as validation error (list of errors)
                    try:
                        validation_error = HTTPValidationError(**error_data)
                        raise OpenfilesValidationError(validation_error)
                    except Exception:
                        # If validation error parsing fails, use generic API error
                        raise OpenfilesAPIError(response.status_code, error_data)

                # Other JSON error responses
                raise OpenfilesAPIError(response.status_code, error_data)

            except (ValueError, TypeError):
                # If not JSON or not matching our error model
                raise OpenfilesHTTPError(response.status_code, response.text)

        # If we got here, the response was successful
        if response.headers.get("Content-Type") == "application/json":
            return response.json()

        return response.content

    def _format_validation_errors(self, validation_error: HTTPValidationError) -> str:
        """
        Format validation errors for better readability.

        Args:
            validation_error: The HTTPValidationError object

        Returns:
            A formatted string with validation errors
        """
        if not validation_error.detail:
            return "Unknown validation error"

        errors = []
        for error in validation_error.detail:
            location = " -> ".join(str(loc) for loc in error.loc)
            errors.append(f"{location}: {error.msg} ({error.type})")

        return "\n".join(errors)

    def upload_file(self, file_path: Union[str, Path], description: str) -> BagResponse:
        """
        Upload a file to TON storage.

        Args:
            file_path: Path to the file to upload
            description: Description of the file

        Returns:
            BagResponse with the bag_id
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        url = f"{self.base_url}/api/files/upload"

        with open(file_path, "rb") as file:
            files = {"file": (file_path.name, file)}
            data = {"description": description}

            response = requests.post(
                url, headers=self._get_headers(), files=files, data=data
            )

            response_data = self._handle_response(response)
            return BagResponse(**response_data)

    def upload_folder(
        self, folder_path: Union[str, Path], description: str
    ) -> BagResponse:
        """
        Upload a folder to TON storage.

        Args:
            folder_path: Path to the folder to upload
            description: Description of the folder

        Returns:
            BagResponse with the bag_id
        """
        folder_path = Path(folder_path)
        if not folder_path.exists() or not folder_path.is_dir():
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        # Create a temporary zip file of the folder
        import tempfile
        import zipfile

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, folder_path)
                        zipf.write(file_path, arcname)

            url = f"{self.base_url}/api/folders/upload"

            with open(temp_path, "rb") as file:
                files = {"file": (folder_path.name + ".zip", file)}
                data = {"description": description}

                response = requests.post(
                    url, headers=self._get_headers(), files=files, data=data
                )

                response_data = self._handle_response(response)
                return BagResponse(**response_data)
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def delete_file(self, bag_id: str) -> None:
        """
        Delete a file from TON storage.

        Args:
            bag_id: ID of the bag to delete
        """
        url = f"{self.base_url}/api/bag"

        data = {"bag_id": bag_id}

        response = requests.delete(url, headers=self._get_headers(), data=data)

        self._handle_response(response)

    def download_file(
        self, bag_id: str, destination: Optional[Union[str, Path]] = None
    ) -> Union[bytes, str]:
        """
        Download a file from TON storage.

        Args:
            bag_id: ID of the bag to download
            destination: Optional path to save the file to

        Returns:
            File content as bytes if destination is None, otherwise the path to
            the saved file
        """
        url = f"{self.base_url}/api/bag/download/{bag_id}"

        response = requests.get(url, headers=self._get_headers(), stream=True)

        content = self._handle_response(response)

        if destination:
            destination = Path(destination)

            # If destination is a directory, use the filename from header
            if destination.is_dir():
                filename = self._get_filename_from_headers(response.headers)
                destination = destination / filename

            with open(destination, "wb") as f:
                if isinstance(content, bytes):
                    f.write(content)
                else:
                    f.write(content.encode())

            return str(destination)

        return content

    def _get_filename_from_headers(self, headers: Dict[str, str]) -> str:
        """
        Extract filename from Content-Disposition header.

        Args:
            headers: Response headers

        Returns:
            Extracted filename or default name
        """
        content_disposition = headers.get("Content-Disposition", "")

        if "filename=" in content_disposition:
            import re

            filename_match = re.search(r'filename="?([^"]+)"?', content_disposition)
            if filename_match:
                return filename_match.group(1)

        return "downloaded_file"

    def get_user_info(self) -> UserResponse:
        """
        Get user information.

        Returns:
            UserResponse with user information
        """
        url = f"{self.base_url}/api/user"

        response = requests.get(url, headers=self._get_headers())

        response_data = self._handle_response(response)
        return UserResponse(**response_data)

    def get_user_files_list(self) -> List[FileInfoResponse]:
        """
        Get the list of user files.

        Returns:
            List of FileInfoResponse objects
        """
        url = f"{self.base_url}/api/user/files_list"

        response = requests.get(url, headers=self._get_headers())

        response_data = self._handle_response(response)
        return [FileInfoResponse(**item) for item in response_data]

    def add_by_bag_id(self, bag_id: str) -> None:
        """
        Add a file by bag ID.

        Args:
            bag_id: ID of the bag to use
        """
        url = f"{self.base_url}/api/bag/add_by_id"

        data = {"bag_id": bag_id}

        response = requests.post(url, headers=self._get_headers(), data=data)

        self._handle_response(response)
