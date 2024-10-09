from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()
API_TOKEN = os.getenv("capsule_api")
BASE_URL = 'https://api.capsulecrm.com/api/v2/'

def make_post_request(endpoint, body):
    """
    Makes a POST request to the Capsule API.

    :param endpoint: The API endpoint (e.g., 'entries/').
    :param body: The JSON data to be sent in the request.
    :return: Response from the Capsule API.
    """
    url = BASE_URL + endpoint
    print(f"Uploading data to {url}...")
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        # Using json=body directly without needing json.dumps()
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content.decode()}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error uploading data to {endpoint}: {e}")
        return None
    

# Utility function to make GET requests to Capsule CRM
def make_get_request(endpoint):
    """
    Makes a GET request to the Capsule API.

    :param endpoint: The API endpoint to target (e.g., 'parties', 'opportunities').
    return: JSON response from the API if successful, otherwise None.
    """
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(BASE_URL + endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()
        # print(f"Data received from {endpoint}: {data}") 
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {endpoint}: {e}")
        return None