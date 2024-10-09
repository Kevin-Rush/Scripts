from colorama import Fore
import autogen
from autogen import config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import UserProxyAgent

from . import agents

config_list = config_list_from_json("OAI_CONFIG_LIST")

def return_reseacher_responses(chat_history):
    # Extract all messages from the researcher in order
    researcher_messages = [message['content'] for message in chat_history if message.get('name') == 'researcher']
    return researcher_messages


def start_converstation(user_proxy, agents, message):
    print(f"{Fore.YELLOW}---------------------Create groupchat---------------------{Fore.RESET}")

    groupchat = autogen.GroupChat(agents=agents, messages=[], max_round=15)

    group_chat_manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})
    print(message)
    response = user_proxy.initiate_chat(group_chat_manager, clear_history=True, message=message, silent=False)
    response_researcher = return_reseacher_responses(response.chat_history)
    # print(response_researcher)

    return response_researcher