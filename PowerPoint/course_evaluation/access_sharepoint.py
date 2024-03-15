import os
import sharepy

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

#read in the username, password, and sharepoint link from a file
with open("sharepoint_credentials.txt", "r") as file:
    username = file.readline().strip()
    password = file.readline().strip()
    site_url = file.readline().strip()
    folder_url = file.readline().strip()

ctx_auth = AuthenticationContext(site_url)
print('Authenticating...')
if ctx_auth.acquire_token_for_user(username, password):
    print('Authenticated')
    ctx = ClientContext(site_url, ctx_auth)
    folder = ctx.web.get_folder_by_server_relative_url(folder_url)
    print('Getting folder...')
    ctx.load(folder)
    print('Loading folder...')
    ctx.execute_query()
    print('Folder URL: ', folder.properties['ServerRelativeUrl'])
else:
    print(ctx_auth.get_last_error())