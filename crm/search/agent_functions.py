import os
import requests
import json
from colorama import Fore
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from bs4 import BeautifulSoup 
from langchain.chat_models import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
import datetime

load_dotenv()
serper_api_key = os.getenv("SL2_SERP_API_KEY")


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