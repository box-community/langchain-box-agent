from box_ai_agents_toolkit import BoxClient, get_ccg_client
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

from src.langchain_box_agent.box_agent import LangChainBoxAgent


def test_box_agent_chat_model_simple():
    client: BoxClient = get_ccg_client()
    model = init_chat_model("gpt-4", model_provider="openai")

    box_agent = LangChainBoxAgent(client, model)

    response = box_agent.chat.invoke(
        {"messages": [HumanMessage(content="hello world")]}
    )

    messages = response.get("messages", [])
    assert messages != []
    assert any("hello".lower() in message.content.lower() for message in messages)
