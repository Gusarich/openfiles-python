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
print("File downloaded")

# Delete a file
client.delete_file(bag_id=file_bag_id)
print("File deleted")

# Import file by bag ID
client.add_by_bag_id(
    bag_id="85d0998dcf325b6fee4f529d4dcf66fb253fc39c59687c82a0ef7fc96fed4c9f"
)
print("File imported")

# Delete file
client.delete_file(
    bag_id="85d0998dcf325b6fee4f529d4dcf66fb253fc39c59687c82a0ef7fc96fed4c9f"
)
print("File deleted")
