#!/usr/bin/env python3
"""
Quick launch script for the LangChain Box Agent Demo.
This automatically launches the demo in simulated mode (no real Box connection).
"""

# Import required components
from agent_implementations import RealBoxAgent
from langchain.chat_models import init_chat_model
from langchain_box_agent_ui import LangChainBoxAgentUI

from langchain_box_agent.box.box_authentication import get_ccg_client
from langchain_box_agent.box_agent import LangChainBoxAgent

if __name__ == "__main__":
    # Initialize Box client
    client = get_ccg_client()

    # Get user info for status message
    user_info = client.users.get_user_me()
    status_message = f"Connected as: {user_info.name}"

    # Initialize language model
    model = init_chat_model("gpt-4", model_provider="openai")

    # Create the Box agent
    langchain_agent = LangChainBoxAgent(client, model)

    # Wrap in our agent interface
    agent = RealBoxAgent(langchain_agent)

    # Start the UI with the simulated agent
    app = LangChainBoxAgentUI(agent, status_message="Real Mode (Box Agent)")
    app.mainloop()
