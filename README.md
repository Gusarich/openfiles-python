# Openfiles Python SDK

A Python SDK for interacting with the Openfiles API.

## Installation

```bash
pip install openfiles-python
```

## Usage

```python
from openfiles import OpenfilesClient

# Method 1: Initialize the client with your API token
client = OpenfilesClient(api_token="your_api_token")

# Method 2: Initialize using OPENFILES_API_TOKEN environment variable
# export OPENFILES_API_TOKEN="your_api_token"
client = OpenfilesClient()

# Upload a file
response = client.upload_file(
    file_path="test/file.txt", description="My file description"
)
file_bag_id = response.bag_id
print(f"File uploaded with bag_id: {file_bag_id}")

# Get user information
user_info = client.get_user_info()
print(f"Space left: {user_info.space_left} / {user_info.capacity}")

# List user files
files = client.get_user_files_list()
for file in files:
    print(f"File: {file.filename}, Size: {file.size}, Bag ID: {file.bag_id}")

# Download a file
client.download_file(bag_id=file_bag_id, destination="test/file_copy.txt")

# Delete a file
client.delete_file(bag_id=file_bag_id)
```

## Features

-   Upload files
-   Download files
-   Delete files
-   Get user information
-   List user files

## License

[MIT License](LICENSE)
