import time

from .api_handling import make_get_request
from .api_handling import make_post_request

def upload_note_to_professor(professor_id, note_content):
    """
    Uploads a note to a specific professor.

    :param professor_id: The ID of the professor (person).
    :param note_content: The content of the note to be uploaded.
    :return: Response from the Capsule API.
    """
    endpoint = 'entries/'

    # Correct payload format based on the documentation
    body = {
        "entry": {
            "type": "note",
            "party": {
                "id": professor_id
            },
            "activityType": -1,
            "content": note_content
        }
    }

    print(f"Uploading note to professor with ID {professor_id}")
    response = make_post_request(endpoint, body)
    return response



# Function to get a list of parties (people and organizations)
def get_parties():
    """
    Fetches all parties (people and organizations) from the Capsule API.

    return: JSON object containing the list of parties.
    """
    return make_get_request('parties')

def get_person_by_name(full_name):
    """
    Fetches a person based on their full name.

    :param full_name: The full name of the person (e.g., "John Doe").
    :return: The person's details as a dictionary, or None if not found.
    """
    page = 1
    more_pages = True
    while more_pages:
        parties_data = make_get_request(f'parties?page={page}')
        if parties_data and 'parties' in parties_data:
            for party in parties_data['parties']:
                if party['type'] == 'person':
                    person_name = f"{party.get('firstName', '')} {party.get('lastName', '')}".strip()
                    if person_name.lower() == full_name.lower():
                        return party
            if len(parties_data['parties']) < 50:
                more_pages = False
            else:
                page += 1
        else:
            more_pages = False
    print(f"Person named {full_name} not found.")
    return None

def get_person_by_id(person_id):
    """
    Fetches a person based on their Capsule CRM ID.

    :param person_id: The ID of the person.
    :return: The person's details as a dictionary, or None if not found.
    """
    return make_get_request(f'parties/{person_id}')

def get_notes_for_party_by_id(party_id):
    """
    Fetches all notes for a specific party (person or organization) by ID, handling pagination.

    :param party_id: The ID of the party (person or organization).
    :return: List of notes related to the party.
    """
    all_notes = []
    page = 1
    more_pages = True

    while more_pages:
        notes_data = make_get_request(f'parties/{party_id}/entries?page={page}')
        if notes_data and 'entries' in notes_data:
            all_notes.extend(notes_data['entries'])
            if len(notes_data['entries']) < 50:
                more_pages = False
            else:
                page += 1
        else:
            more_pages = False
    return all_notes

def get_party_id(college_name):
    """
    Fetches the party ID for a given college name.

    :param college_name: The name of the college to search for.
    :return: The ID of the college party, or None if not found.
    """
    parties = make_get_request('parties')
    if parties and 'parties' in parties:
        for party in parties['parties']:
            if party.get('name') == college_name:
                return party['id']
    return None

def get_all_people():
    """
    Fetches all people (professors) from the Capsule API, handling pagination.
    
    :return: List of people (professors).
    """
    people = []
    page = 1
    more_pages = True

    while more_pages:
        parties_data = make_get_request(f'parties?page={page}')
        
        if parties_data and 'parties' in parties_data:
            for party in parties_data['parties']:
                if party['type'] == 'person' and party.get('organisation'):
                    people.append(party)
            
            if len(parties_data['parties']) < 50:
                more_pages = False
            else:
                page += 1
        else:
            more_pages = False

    return people

def get_party_name(entry, is_professor, professor_name):
    """
    Returns the party name based on whether it's a professor or an organization.

    :param entry: Entry data for the note.
    :param is_professor: Boolean indicating if the party is a professor.
    :param professor_name: Name of the professor.
    :return: The party's name.
    """
    if is_professor:
        return professor_name
    return entry['party'].get('name', 'Unknown party')

def get_notes_for_people(people):
    """
    Fetches notes for each person (professor) associated with a college, handling pagination.

    :param people: List of people dictionaries (professors).
    :return: List of notes related to all people (professors).
    """
    all_notes = []

    for person in people:
        person_id = person['id']
        person_name = f"{person.get('firstName', 'Unknown')} {person.get('lastName', 'Unknown')}"
        print(f"Fetching notes for {person_name} (ID: {person_id})")

        # Use the paginated_get_request function to fetch paginated notes
        notes = paginate_get_request(f'parties/{person_id}/entries')
        
        if notes:
            # Extract notes and associate them with the professor's name
            professor_note_summaries = extract_note_details({'entries': notes}, is_professor=True, professor_name=person_name)
            all_notes.extend(professor_note_summaries)

        if not all_notes:
            print(f"No notes found for {person_name}")

    return all_notes