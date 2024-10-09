import time

from colorama import Fore
from .api_handling import make_get_request
from .api_handling import make_post_request

def upload_note_to_college(college_id, note_content):
    """
    Uploads a note to a specific college (organization).

    :param college_id: The ID of the college (organization).
    :param note_content: The content of the note to be uploaded.
    :return: Response from the Capsule API.
    """
    endpoint = 'entries/'  # This is the correct endpoint for creating an entry (note)

    body = {
        "entry": {
            "type": "note",
            "party": {
                "id": college_id
            },
            "activityType": -1,  # Based on Capsule CRM docs for notes
            "content": note_content
        }
    }

    print(f"Uploading note to college (organization) with ID {college_id}")
    response = make_post_request(endpoint, body)
    return response



def get_organizations(name_filter=None):
    """
    Fetches all organizations from the Capsule API, with an optional filter for organization name.
    
    :param name_filter: Optional. If provided, only organizations matching the name_filter will be returned.
    :return: List of organizations (filtered if name_filter is provided).
    """
    organizations = []
    page = 1
    more_pages = True

    while more_pages:
        parties_data = make_get_request(f'parties?page={page}')

        if parties_data and 'parties' in parties_data:
            for party in parties_data['parties']:
                if party['type'] == 'organisation':
                    # If name_filter is provided, filter organizations by name
                    if name_filter:
                        if party.get('name', '').lower() == name_filter.lower():
                            return party  # Return immediately if specific org found by name
                    else:
                        organizations.append(party)

            # Continue if there are still 50 parties retrieved (i.e., more pages)
            if len(parties_data['parties']) < 50:
                more_pages = False
            else:
                page += 1
        else:
            more_pages = False

    if name_filter:
        print(f"Organization named {name_filter} not found.")
        return None

    return organizations


def get_notes_for_college(college_id):
    """
    Fetches all notes (entries) associated with a specific college by querying the related party ID.

    :param college_id: The ID of the college (organisation) party.
    :return: List of notes associated with the college.
    """
    endpoint = f'parties/{college_id}/entries'
    notes = make_get_request(endpoint)
    return notes

def get_people_in_org(org_id, return_ids_only=False):
    """
    Fetches all people (professors) associated with a specific organization (college), with an option to return either IDs or full details.
    
    :param org_id: The ID of the organization (college).
    :param return_ids_only: Boolean flag indicating if only IDs should be returned (True) or full details (False).
    :return: List of professor party IDs or full details associated with the organization.
    """
    people = []
    page = 1  # Start with page 1
    more_pages = True

    while more_pages:
        # Fetch parties page by page
        parties_data = make_get_request(f'parties?page={page}')
        
        if parties_data and 'parties' in parties_data:
            print(f"Page {page}: Retrieved {len(parties_data['parties'])} parties.")
            
            for party in parties_data['parties']:
                if party['type'] == 'person' and party.get('organisation') and party['organisation'].get('id') == org_id:
                    if return_ids_only:
                        people.append(party['id'])  # Return only IDs
                    else:
                        people.append(party)  # Return full details
            
            if len(parties_data['parties']) < 50:  # Assume no more results if less than 50
                more_pages = False
            else:
                page += 1  # Continue to the next page
                time.sleep(1)  # Respect API rate limits
        else:
            more_pages = False

    return people

def get_all_organizations():
    """
    Fetches all organizations from the Capsule API, handling pagination.
    
    :return: List of organizations.
    """
    organizations = []
    page = 1
    more_pages = True

    while more_pages:
        parties_data = make_get_request(f'parties?page={page}')

        if parties_data and 'parties' in parties_data:
            for party in parties_data['parties']:
                if party['type'] == 'organisation':
                    organizations.append(party)
            # Continue if there are still 50 parties retrieved (i.e. more pages)
            if len(parties_data['parties']) < 50:
                more_pages = False
            else:
                page += 1
        else:
            more_pages = False

    return organizations

def get_org_by_id(org_id):
    """
    Fetches a person based on their Capsule CRM ID.

    :param person_id: The ID of the person.
    :return: The person's details as a dictionary, or None if not found.
    """
    return make_get_request(f'parties/{org_id}')