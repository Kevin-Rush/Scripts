import re
import pandas as pd

def extract_text_between_markers(text, start_marker, end_marker):
    pattern = rf"{re.escape(start_marker)}(.+?){re.escape(end_marker)}"
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    else:
        return None

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
    print(df.iloc[-1])

df.to_csv('extracted_log_data.csv', index=False)