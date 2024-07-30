import requests
import pandas as pd

def save_file_as_dataframe(file_path):
    data = {'File': [], 'Slide Number': [], 'Title': [], 'Subtitle': [], 'Slide Text': [], 'Notes Text': []}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith("File:"):
                data['File'].append(line[6:])
            elif line.startswith("Slide Number:"):
                data['Slide Number'].append(line[14:])
            elif line.startswith("Title:"):
                data['Title'].append(line[7:])
            elif line.startswith("Subtitle:"):
                data['Subtitle'].append(line[10:])
            elif line.startswith("Slide Text:"):
                data['Slide Text'].append(line[12:])
            elif line.startswith("Notes Text:"):
                data['Notes Text'].append(line[12:])
    df = pd.DataFrame(data)
    return df

def extract_links_txt(file_path):
    links = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.split()
            for word in words:
                if word.startswith("http"):
                    links.append(word)
                    print(word)
    return links

def check_link(link):
    try:
        response = requests.head(link)
        print(f"Link: {link} - Response: {response.status_code}")
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Link: {link} - Error: {e}")
        return e

# Call the function to save the file as a pandas dataframe
df = save_file_as_dataframe("course_info.txt")
print(df)

# Call the function to extract links from the text file
links = extract_links_txt("course_info.txt")
for link in links:
    check_link(link)
    
