from openfiles import OpenfilesClient


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
