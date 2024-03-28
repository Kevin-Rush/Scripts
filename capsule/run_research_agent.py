from utils import find_orgs

import os
from colorama import Fore
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from bs4 import BeautifulSoup 
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import json
from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import UserProxyAgent
import autogen

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



load_dotenv()
#brwoserless_api_key = os.getenv("BROWSERLESS_API_KEY")
serper_api_key = os.getenv("SERP_API_KEY")
airtable_api_key = os.getenv("AIRTABLE_API_KEY")
config_list = config_list_from_json("OAI_CONFIG_LIST")


# ------------------ Create functions ------------------ #

# Function for google search
def google_search(search_keyword):    
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": search_keyword
    })

    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"{Fore.GREEN}---------------------Search Complete---------------------{Fore.RESET}")
    print("RESPONSE:", response.text)
    return response.text

# Function for scraping
def summary(objective, content):
    llm = ChatOpenAI(temperature = 0, model = "gpt-3.5-turbo-16k-0613")

    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size = 10000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    
    map_prompt = """
    Write a summary of the following text for {objective}:
    "{text}"
    SUMMARY:
    """
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "objective"])
    
    summary_chain = load_summarize_chain(
        llm=llm, 
        chain_type='map_reduce',
        map_prompt = map_prompt_template,
        combine_prompt = map_prompt_template,
        verbose = False
    )

    output = summary_chain.run(input_documents=docs, objective=objective)

    return output

def web_scraping(objective: str, url: str):
    #scrape website, and also will summarize the content based on objective if the content is too large
    #objective is the original objective & task that user give to the agent, url is the url of the website to be scraped

    print("Scraping website...")

    response = selinium_scrape(url)
    print(f"{Fore.YELLOW}---------------------Scrape Response---------------------{Fore.RESET}")
    #write the response to a file
    with open("scraped_response.txt", "a", encoding='utf-8') as f:  
        f.write(response)

    if response != "":
        soup = BeautifulSoup(response, "html.parser")
        text = soup.get_text()
        text = clean_soup_text(text)
        #add text to a file
        with open("scraped_text.txt", "a", encoding='utf-8') as f:
            f.write(text)

        if len(text) > 10000:
            output = summary(objective, text)
            return output
        else:
            return text
    else:
        print(f"{Fore.RED}HTTP request failed with status code {response}{Fore.RESET}")      

def selinium_scrape(url):

    # Using WebDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(url)

    # Check the current URL
    current_url = driver.current_url
    print(f"{Fore.GREEN}Current URL:", current_url, f"{Fore.RESET}")

    page_content = driver.page_source

    #write page_content to a file
    with open("page_content.txt", "a", encoding='utf-8') as f:
        f.write(page_content)

    driver.quit()

    return page_content

def clean_soup_text(text):
    # Remove all the newlines
    text = text.replace("\n", " ")
    # Remove all the extra spaces
    text = " ".join(text.split())
    return text

# Function for get airtable records
def get_airtable_records(base_id, table_id):
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"

    headers = {
        'Authorization': f'Bearer {airtable_api_key}',
    }

    response = requests.request("GET", url, headers=headers)
    print(f"{Fore.GREEN}---------------------Airtable Response---------------------{Fore.RESET}")
    data = response.json()
    print(data)
    return data


# # Function for update airtable records

def update_single_airtable_record(base_id, table_id, id, fields):
    url = f"https://api.airtable.com/v0/{base_id}/{table_id}"

    headers = {
        'Authorization': f'Bearer {airtable_api_key}',
        "Content-Type": "application/json"
    }

    data = {
        "records": [{
            "id": id,
            "fields": fields
        }]
    }

    response = requests.patch(url, headers=headers, data=json.dumps(data))
    data = response.json()
    return data


# ------------------ Create agent ------------------ #

# Create user proxy agent
user_proxy = UserProxyAgent(name="user_proxy",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=1
    )

# Create researcher agent
researcher = GPTAssistantAgent(
    name = "researcher",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_Nt9WR0jReC1JgQ88fYJEjwAg"
    }
)

researcher.register_function(
    function_map={
        "web_scraping": web_scraping,
        "google_search": google_search
    }
)

# Create research manager agent
research_manager = GPTAssistantAgent(
    name="research_manager",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_Qn0WmtmBn6gl9eJRursaWfrX"
    }
)


# Create director agent
director = GPTAssistantAgent(
    name = "director",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_7QUrlJsRwLo4aEAPh8ijYI2R",
    }
)

director.register_function(
    function_map={
        "get_airtable_records": get_airtable_records,
        "update_single_airtable_record": update_single_airtable_record
    }
)


# Create group chat
# groupchat = autogen.GroupChat(agents=[user_proxy, researcher, research_manager, director], messages=[], max_round=15)

groupchat = autogen.GroupChat(agents=[user_proxy, researcher, research_manager], messages=[], max_round=15)

group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})


# ------------------ start conversation ------------------ #
# message = """
# Research to find the status of all AI programs for the community colleges in the list: https://airtable.com/appXWlxTsOhTOixhx/tblFNR8gRkGun5Ky6/viwxUWeJGthCmyIv9?blocks=hide
# """

orgs = find_orgs("contacts-2024-03-25.csv")

#drop first element
orgs.pop(0)

for i in orgs:
    print(f"{Fore.YELLOW}---------------------Searching for {i}---------------------{Fore.RESET}")
    print(i)
    message = f"Research for student or community projects, initiatives, or any positive story from {i} in the field of AI."

    user_proxy.initiate_chat(group_chat_manager, message=message)
    print(f"{Fore.GREEN}---------------------Search for {i} Complete---------------------{Fore.RESET}")
    break
