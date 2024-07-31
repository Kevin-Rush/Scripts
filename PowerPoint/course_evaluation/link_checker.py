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

def check_links_in_dataframe(df):
    for index, row in df.iterrows():
        row_values_string = ' '.join(str(value) for value in row.values)
        words = row_values_string.split()
        for w in words:
            if w.startswith("http"):
                print(f"File: {row['File']}\nSlide Number: {row['Slide Number']}\nTitle: {row['Title']}\nSubtitle: {row['Subtitle']}\nSlide Text: {row['Slide Text']}\nNotes Text: {row['Notes Text']}")
                print(f"Link: {w} - Response: {check_link(w)}")
                print()

def check_link(link):
    try:
        response = requests.head(link)
        # print(f"Link: {link} - Response: {response.status_code}")
        return response.status_code
    except requests.exceptions.RequestException as e:
        # print(f"Link: {link} - Error: {e}")
        return e

# Call the function to save the file as a pandas dataframe
df = save_file_as_dataframe("course_info.txt")
print(df)

# Call the function to check links in the dataframe
check_links_in_dataframe(df)

# # Call the function to extract links from the text file
# links = extract_links_txt("course_info.txt")
# print(links)
# # Save the dataframe to a CSV file
# df.to_csv("output.csv", index=False)

# for link in links:
#     response = check_link(link)
#     print(type(response))
#     print(response)
#     if response != 200:
#         for index, row in df.iterrows():
#             if link in row.values:
#                 print(f"Link {link} found in row {index}")
#                 print(row.values)
#                 exit()