# Import required components
from box_ai_agents_toolkit import get_ccg_client
from langchain.chat_models import init_chat_model

from langchain_box_agent.box_agent import LangChainBoxAgent

# Initialize Box client
client = get_ccg_client()

# Get user info for status message
user_info = client.users.get_user_me()
status_message = f"Connected as: {user_info.name}"

# Initialize language model
model = init_chat_model("gpt-4", model_provider="openai")

# Create the Box agent
box_agent = LangChainBoxAgent(client, model, use_internal_memory=False)

react_agent = box_agent.react_agent
