import csv

# def extract_emails(file_path):
#     emails = []
#     i = 0
#     with open(file_path, 'r') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             print(i)
#             print(row[2])
#             if row[0] != "" and row[2] != 'emailAddresses':
#                 emails.append(process_emailAddress_entry(row[2]))  # Assuming email is in the third column (index 2)
#             i += 1
                
#     return emails

# def process_emailAddress_entry(str):
#     #remove all text prior to the @ symbol
#     str = str.split('@')[1]
#     #remove all text after a '
#     str = str.split('\'')[0]
#     return str

def remove_duplicates(var_list):
    #remove duplicates in the list
    return list(set(var_list))   
    
def find_orgs(file):
    orgs = []
    with open(file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'Organization':
                orgs.append(row[2])  # Assuming organization is in the second column (index 1)
                
    return orgs

full_csv = "contacts-2024-03-25.csv"
orgs = find_orgs(full_csv)

#save emails to a text file
with open('orgs.txt', 'w') as file:
    for org in orgs:
        if org is not None:
            file.write(org + '\n')

# file_path = 'participants.csv' 
# # emails = extract_emails(file_path)
# print(emails)

# emails = remove_duplicates(emails)

# #save emails to a text file
# with open('emails.txt', 'w') as file:
#     for email in emails:
#         if email is not None:
#             file.write(email + '\n')