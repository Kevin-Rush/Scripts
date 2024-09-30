import re
import os

def check_url_presence(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
        return len(urls) > 0


directory = r'C:\Users\kevin\Documents\Coding\Scripts\capsule\0908_Microsoft'
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        result = check_url_presence(file_path)
        print(f"{filename}: {result}")

        if not result:
            os.remove(file_path)