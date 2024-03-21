import os
import sharepy
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential


#read in the username, password, and sharepoint link from a file
with open("sharepoint_credentials.txt", "r") as file:
    username = file.readline().strip()
    password = file.readline().strip()
    sharepoint_url = file.readline().strip()
    folder_url = file.readline().strip()


user_credential = UserCredential(username, password)
ctx = ClientContext(sharepoint_url).with_credentials(user_credential)

folder = ctx.web.get_folder_by_server_relative_url(folder_url)
ctx.load(folder)
try:
    ctx.execute_query()
    print("Access to the folder is successful!")
    print("Folder properties: ", folder.properties)
except Exception as e:
    print("Failed to access the folder. Error: ", e)