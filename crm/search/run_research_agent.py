import os
from colorama import Fore
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from bs4 import BeautifulSoup 
from langchain.chat_models import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
import datetime

from .agent_management import start_converstation
from . import agents


#read a text file
with open("orgs.txt", "r") as file:
    orgs = [line.strip() for line in file]

prompts = [
    "What EU or France grants are there to help AI programs at Business Schools in France?"
    # "Research for any government funding (federal, state, or local grants) for the AI program at {i}. Please exclude any funding from private companies! I only want government funding.",
    # "Research for any student success stories (projects, awards, competitions, etc.) from the AI program at {i}. I must stress that I only want you to find stories about AI and from 2024, I DO NOT WANT ANY stories older than 2024!",
    # "Research for the enrollment numbers for the AI program at {i}. Please be very careful to ONLY report enrollment numbers for the AI program NOT any other program or the entire school.",
    # "Research for the number of AI degrees awarded by {i}. Please be very careful to ONLY report on the number of degrees awarded for the AI program NOT any other program or the entire school.",
    # "Research for the number of AI certificates awarded by {i}.",
    # "Research for any news about NVIDIA collaborating with {i} on an AI program. Only report stories about the AI program from {i} and NVIDIA, I don't want any stroeis about NVIDIA collaborating on any other program with any other college.",
    # "Research for any news about AMD collaborating with {i} on an AI program. Only report stories about the AI program from {i} and NVIDIA, I don't want any stroeis about NVIDIA collaborating on any other program with any other college.",
    # "Research for any news about Microsoft collaborating with {i} on an AI program. Only report stories about the AI program from {i} and Microsoft, I don't want any stroeis about Microsoft collaborating on any other program with any other college.",
    # "Research for any news about AWS collaborating with {i} on an AI program. Only report stories about the AI program from {i} and AWS, I don't want any stroeis about AWS collaborating on any other program with any other college.",
    # "What is the AACSB AI Conference with the neoma business school about?",
    # "What is going to be discussed at the AACSB AI Conference with the neoma business school?",
    # "Who will be attending the AACSB AI Conference with the neoma business school?",
    # "What is the purpose of the AACSB AI Conference with the neoma business school?",
    # "What is the best way for a small AI consultant to get the most out of the AACSB AI Conference with the neoma business school?",
    # "What opportunities are there for an Ed Tech company to leverage attending the AACSB AI Conference with the neoma business school?",
]


# What colleges are trying to make statewide movements with AI
# What is the status of our college's AI labs?
# What grants could community colleges apply to help their AI program?


k = 0
college_search = input("Do you want to search for colleges? (y/n): ")

for p in prompts:
    k += 1
    print(f"{Fore.YELLOW}---------------------{p}---------------------{Fore.RESET}")

    if college_search == "y":
        for i in orgs:
            print(f"{Fore.YELLOW}---------------------Searching for {i}---------------------{Fore.RESET}")
            print(i)
            p = f"{p.format(i=i)}"

            try:
                user_proxy = agents.create_user_proxy()
                agents = [user_proxy, agents.create_researcher(), agents.create_research_manager()]
                response_researcher = start_converstation(user_proxy, agents, message=p)

                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                file_name = f"{k}_prompt_log_{current_date}_{i}.txt"

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
    else:
        try:
            user_proxy = agents.create_user_proxy()
            agnets = [user_proxy, agents.create_researcher(), agents.create_research_manager()]

            response_researcher = start_converstation(user_proxy, agnets, message=p)

            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            file_name = f"{k}_prompt_log_2_{current_date}.txt"

            with open(file_name, "w") as file:
                for response in response_researcher:
                    file.write(response + "\n")

        except ValueError as e:
            print(f"{Fore.RED}ValueError occurred while processing{e}{Fore.RESET}")
            continue  # Continue with the next iteration
        except AssertionError as e:
            print(f"{Fore.RED}AssertionError occurred while processing{e}{Fore.RESET}")
            continue  # Continue with the next iteration
        except Exception as e:
            print(f"{Fore.RED}An unexpected error occurred while processing {e}{Fore.RESET}")
            continue  # Continue with the next iteration
            
