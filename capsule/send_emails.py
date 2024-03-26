import smtplib
import pandas as pd

def replace_name(message, email):
    #load the csv file participants.csv as a df
    df = pd.read_csv('participants.csv')

    #find the email address in the df and get the first and last name
    name = df[df['emailAddresses'] == email]['firstName'].values[0]
    if "(" in name:
        name = name.split(" (")[0]
    print(name)
    return message.replace('NAME', name)

def replace_college(message, email):
    df = pd.read_csv('participants.csv')
    return df[df['emailAddresses'] == email]['organisation'].values[0]

# Email credentials
sender_email = 'kevin@sustainablelivinglab.org'
sender_app_password = 'czoe yrum xltd abhr'

# Read emails from file
print("For safety this script has been ended early.")
exit()
with open('emails_addresses.txt', 'r') as file:
    recipients = file.readlines()

#remove any /n from all entries in emails
recipients = [email.strip() for email in recipients]

#remove all duplicates
recipients = list(set(recipients))
df = pd.read_csv('participants.csv')

# Email content
subject = 'ENTER_SUBJECT'
#the text inside the file email_text.txt
with open('email_text.txt', 'r') as file:
    message = file.read()

smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtpserver.ehlo()
smtpserver.login(sender_email, sender_app_password)

# Test send mail
sent_from = sender_email
i = 0
print(recipients)
for email in recipients:
    print(f"Sending email to {email}, emails sent: {i}")
    i += 1
    message = replace_name(message, email)
    sent_to = email
    email_text = message
    smtpserver.sendmail(sent_from, sent_to, email_text)

# Close the connection
smtpserver.close()