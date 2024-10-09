from colorama import Fore
import os
import time

from . import note_handling as notes_fns 
from . import party_functions as party_fns 
from . import org_functions as org_fns 

def main():
    # Test uploading a note to a professor
    professor_id = 230524703  # Replace with a valid professor ID
    professor_name = "Gerald Aska"
    note_content_prof = "This is a test note for Gerald Aska."
    response_professor = party_fns.upload_note_to_professor(professor_id, note_content_prof)
    
    if response_professor:
        print(Fore.GREEN + f"Successfully uploaded note to professor (ID: {professor_id}).")
    else:
        print(Fore.RED + f"Failed to upload note to professor (ID: {professor_id}).")
    
    # Test uploading a note to a college
    college_id = 230524702  # Replace with a valid college ID
    college_name = "Morris County Vocational School (New Jersey)"
    note_content_college = "This is a test note for the Morris County Vocational School."
    response_college = org_fns.upload_note_to_college(college_id, note_content_college)
    
    if response_college:
        print(f"{Fore.GREEN}Successfully uploaded note to college (ID: {college_id}).{Fore.RESET}")
    else:
        print(f"{Fore.RED}Failed to upload note to college (ID: {college_id}).{Fore.RESET}")

if __name__ == "__main__":
    main()