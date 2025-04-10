from box_ai_agents_toolkit import BoxClient
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

from src.langchain_box_agent.box_agent import LangChainBoxAgent

load_dotenv()


def test_box_agent_chat_model_simple(box_client_ccg: BoxClient, chat_config: str):
    client = box_client_ccg
    model = init_chat_model("gpt-4", model_provider="openai")

    box_agent = LangChainBoxAgent(client, model, True)

    response = box_agent.react_agent.invoke(
        {"messages": [HumanMessage(content="hello world")]}, chat_config
    )

    messages = response.get("messages", [])
    assert messages != []
    assert any("hello".lower() in message.content.lower() for message in messages)
