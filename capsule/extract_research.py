import re
import pandas as pd

def extract_text_between_markers(text, start_marker, end_marker):
    start_index = text.find(start_marker)
    
    if start_index == -1:
        return None  # Start marker not found

    # Find the end marker after the start marker
    end_index = text.find(end_marker, start_index + len(start_marker))

    if end_index == -1:
        # If end marker is not found, extract up to the next start_marker or end of the file
        next_start_index = text.find('---------------------Searching for', start_index + len(start_marker))
        end_index = next_start_index if next_start_index != -1 else len(text)
    
    extracted_text = text[start_index + len(start_marker):end_index]
    return extracted_text.strip()

with open("orgs.txt", "r") as file:
    orgs = [line.strip() for line in file]

with open('output_0828_graduates.txt', 'r', encoding='UTF-16') as file:
    log_content = file.read()

df = pd.DataFrame(columns=['College', 'Extracted Text'])

for i in orgs:
    start_marker = f"---------------------Searching for {i}---------------------"
    end_marker = f"---------------------Search for {i} Complete---------------------"

    extracted_text = extract_text_between_markers(log_content, start_marker, end_marker)

    df = df.append({'College': i, 'Extracted Text': extracted_text}, ignore_index=True)

# df.to_csv('extracted_log_data.csv', index=False)


print("Length of df:", len(df)) 
print("Number of entries in College:", len(df['College'])) 
print("Number of entries in Extracted Text:", len(df['Extracted Text'])) 
print("Number of null entries in College:", df['College'].isnull().sum()) 
print("Number of null entries in Extracted Text:", df['Extracted Text'].isnull().sum())