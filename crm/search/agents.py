from dotenv import load_dotenv
from colorama import Fore
import autogen
from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import UserProxyAgent

from .agent_functions import web_scraping, google_search

config_list = config_list_from_json("OAI_CONFIG_LIST")

def create_user_proxy():
    print(f"{Fore.YELLOW}---------------------Create user proxy agent---------------------{Fore.RESET}")
    user_proxy = UserProxyAgent(name="user_proxy",
        is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        )
    
    return user_proxy

def create_researcher():
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
        }
    )

    return researcher

def create_research_manager():
    print(f"{Fore.YELLOW}---------------------Create research manager agent---------------------{Fore.RESET}")
    research_manager = GPTAssistantAgent(
        name="research_manager",
        description="Research manager agent",
        llm_config = {
            "config_list": config_list,
            "assistant_id": "asst_Qn0WmtmBn6gl9eJRursaWfrX"
        }
    )

    return research_manager



