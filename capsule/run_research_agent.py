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

from langchain_community.callbacks import get_openai_callback
import datetime
# from langchain_openai import OpenAI

print(f"{Fore.YELLOW}---------------------Loading Environment Varaibles---------------------{Fore.RESET}")

load_dotenv()
os.environ['AUTOGEN_USE_DOCKER'] = '0'
#brwoserless_api_key = os.getenv("BROWSERLESS_API_KEY")
serper_api_key = os.getenv("SL2_SERP_API_KEY")
config_list = config_list_from_json("OAI_CONFIG_LIST")


def return_reseacher_responses(chat_history):
    # Extract all messages from the researcher in order
    researcher_messages = [message['content'] for message in chat_history if message.get('name') == 'researcher']
    return researcher_messages

# ------------------ Create functions ------------------ #

#function to check previously searched urls
def check_url(url):
    # with open("maracopa_searched_urls.txt", "r") as file:
    #     urls = file.readlines()
    #     #add the charachter "\n" to the variable url
    #     url = url + "\n"
    #     print(urls)
    #     print(url in urls)
    #     if url in urls:
    #         print(f"{Fore.RED}---------------------Old URL---------------------{Fore.RESET}")
    #         return False
    #     else:
    #         print(f"{Fore.GREEN}---------------------New URL---------------------{Fore.RESET}")
    #         print(url)
    #         return True
    return True

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
    llm = ChatOpenAI(temperature = 0, model = "gpt-3.5-turbo-0125")

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

    if check_url(url):
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
    else:
        return "URL has been searched before, ignore and move onto the next one."

def selinium_scrape(url, searched_url_file="searched_urls.txt"):

    # Using WebDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(url)

    # Check the current URL
    current_url = driver.current_url
    print(f"{Fore.GREEN}Current URL:", current_url, f"{Fore.RESET}")
    with open(searched_url_file, "a", encoding='utf-8') as f:
            f.write(current_url)
            f.write("\n")

    page_content = driver.page_source

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

 
# Function for update airtable records

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
print(f"{Fore.YELLOW}---------------------Create user proxy agent---------------------{Fore.RESET}")
user_proxy = UserProxyAgent(name="user_proxy",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    )

# Create researcher agent
print(f"{Fore.YELLOW}---------------------Create researcher agent---------------------{Fore.RESET}")
researcher = GPTAssistantAgent(
    name = "researcher",
    description = "Researcher agent",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_Nt9WR0jReC1JgQ88fYJEjwAg"
    }
)

print(f"{Fore.YELLOW}---------------------Register researcher functions---------------------{Fore.RESET}")
researcher.register_function(
    function_map={
        "web_scraping": web_scraping,
        "google_search": google_search,
        "check_url": check_url
    }
)

# Create research manager agent
print(f"{Fore.YELLOW}---------------------Create research manager agent---------------------{Fore.RESET}")
research_manager = GPTAssistantAgent(
    name="research_manager",
    description="Research manager agent",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_Qn0WmtmBn6gl9eJRursaWfrX"
    }
)


# Create director agent
print(f"{Fore.YELLOW}---------------------Create director agent---------------------{Fore.RESET}")
director = GPTAssistantAgent(
    name = "director",
    description = "Director agent",
    llm_config = {
        "config_list": config_list,
        "assistant_id": "asst_7QUrlJsRwLo4aEAPh8ijYI2R",
    }
)

print(f"{Fore.YELLOW}---------------------Register director functions---------------------{Fore.RESET}")
director.register_function(
    function_map={
        "get_airtable_records": get_airtable_records,
        "update_single_airtable_record": update_single_airtable_record
    }
)


# # Create group chat
# groupchat = autogen.GroupChat(agents=[user_proxy, researcher, research_manager, director], messages=[], max_round=15)

print(f"{Fore.YELLOW}---------------------Create groupchat---------------------{Fore.RESET}")

groupchat = autogen.GroupChat(agents=[user_proxy, researcher, research_manager], messages=[], max_round=15)

group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})


# # ------------------ start conversation ------------------ #

# message = f"How many students have graduated with an AI certificate OR degree from Chandler-Gilbert Community College?"

#ask the user to check the searched_urls.txt file
# user_response = input(print("Are you referencing the correct searched_urls file? (Answer y to proceed): "))
# if user_response.lower() != "y":
#     print("Please reference the correct file.")
#     exit()

# message = "What is going on in the US Tech sector? Why are so many tech companies doing poorly?"

# response = user_proxy.initiate_chat(group_chat_manager, clear_history=True, message=message, silent=False)
# # Write response to a text file
# with open("response.txt", "w") as file:
#     file.write(response)
# print(response('chat_history'))

# for i in range(15):
#     print(f"{Fore.YELLOW}---------------------Starting Iterative Search: {i}---------------------{Fore.RESET}")
#     user_proxy.initiate_chat(group_chat_manager, clear_history=True, message=message, silent=False)


# Research for student or community projects, initiatives, or any positive story from {i} in the field of AI. But only report stories from 2023 or 2024


#read a text file
with open("orgs.txt", "r") as file:
    orgs = [line.strip() for line in file]

prompts = [
    #"Research for any government funding (federal, state, or local grants) for the AI program at {i}. Please exclude any funding from private companies! I only want government funding.",
    # "Research for any student success stories (projects, awards, competitions, etc.) from the AI program at {i}. I must stress that I only want you to find stories about AI and from 2024, I DO NOT WANT ANY stories older than 2024!",
    # "Research for the enrollment numbers for the AI program at {i}. Please be very careful to ONLY report enrollment numbers for the AI program NOT any other program or the entire school.",
    # "Research for the number of AI degrees awarded by {i}. Please be very careful to ONLY report on the number of degrees awarded for the AI program NOT any other program or the entire school.",
    "Research for the number of AI certificates awarded by {i}.",
    # "Research for any news about NVIDIA collaborating with {i} on an AI program.",
]



for p in prompts:
    print(f"{Fore.YELLOW}---------------------{p}---------------------{Fore.RESET}")
    for i in orgs:
        print(f"{Fore.YELLOW}---------------------Searching for {i}---------------------{Fore.RESET}")
        print(i)
        message = f"{p.format(i=i)}"

        try:
            # user_proxy.initiate_chat(group_chat_manager, clear_history=True, message=message, silent=False)
            response = user_proxy.initiate_chat(group_chat_manager, clear_history=True, message=message, silent=False)
            response_researcher = return_reseacher_responses(response.chat_history)
            print(response_researcher)

            # Save response_researcher to a file

            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            file_name = f"log_{current_date}_{i}.txt"

            with open(file_name, "w") as file:
                for response in response_researcher:
                    file.write(response + "\n")

        except ValueError as e:
            print(f"{Fore.RED}ValueError occurred while processing {i}: {e}{Fore.RESET}")
            continue  # Continue with the next iteration
        except AssertionError as e:
            print(f"{Fore.RED}AssertionError occurred while processing {i}: {e}{Fore.RESET}")
            continue  # Continue with the next iteration
        except Exception as e:
            print(f"{Fore.RED}An unexpected error occurred while processing {i}: {e}{Fore.RESET}")
            continue  # Continue with the next iteration
        
        print(f"{Fore.GREEN}---------------------Search for {i} Complete---------------------{Fore.RESET}")