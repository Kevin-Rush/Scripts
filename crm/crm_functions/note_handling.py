from .api_handling import make_get_request
from .utils import paginate_get_request, format_attachments
from .party_functions import get_party_name


def extract_note_details(notes_data, is_professor=False, professor_name=""):
    """
    Extracts and organizes details from notes in a more readable format.

    :param notes_data: JSON data containing all the notes.
    :param is_professor: Flag to determine if the notes are for a professor.
    :param professor_name: The name of the professor for professor-related notes.
    :return: List of formatted strings with note details.
    """
    note_details = []

    if 'entries' in notes_data:
        for entry in notes_data['entries']:
            note_content = entry.get('content', 'No content')
            created_at = entry.get('createdAt', 'No creation date')
            creator = entry['creator'].get('name', 'Unknown creator')
            attachments = format_attachments(entry.get('attachments', []))
            party_name = get_party_name(entry, is_professor, professor_name)

            detail = (f"Note Content: {note_content}\n"
                      f"Created At: {created_at}\n"
                      f"Creator: {creator}\n"
                      f"Attachments: {attachments}\n"
                      f"Party: {party_name}\n"
                      "----------------------")
            
            note_details.append(detail)
    
    return note_details



