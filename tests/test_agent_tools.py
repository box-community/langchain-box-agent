from box_ai_agents_toolkit import BoxClient, get_ccg_client
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from src.langchain_box_agent.box_agent import LangChainBoxAgent
from langchain_core.messages import HumanMessage
from src.langchain_box_agent.box_tools import box_who_am_i


def test_agent_tools_external_who_am_i():
    # client: BoxClient = get_ccg_client()
    model = init_chat_model("gpt-4", model_provider="openai")

    # box_agent = LangChainBoxAgent(client, model)

    tools = [box_who_am_i]
    agent_executor = create_react_agent(model, tools)

    response = agent_executor.invoke({"messages": [HumanMessage(content="who am i?")]})

    messages = response.get("messages", [])
    assert messages != []
    assert any("Authenticated" in message.content for message in messages)


def test_agent_tools_who_am_i():
    client: BoxClient = get_ccg_client()
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model)
    response = box_agent.chat.invoke({"messages": [HumanMessage(content="who am i?")]})
    messages = response.get("messages", [])
    assert messages != []
    assert any("Authenticated" in message.content for message in messages)


def test_agent_tools_box_search():
    client: BoxClient = get_ccg_client()
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model)
    response = box_agent.chat.invoke(
        {"messages": [HumanMessage(content="locate my hab-03-01 file by name")]}
    )
    messages = response.get("messages", [])
    assert messages != []
    assert any("hab-03-01" in message.content.lower() for message in messages)


def test_agent_tools_box_read_file_by_id():
    client: BoxClient = get_ccg_client()
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model)
    response = box_agent.chat.invoke(
        {"messages": [HumanMessage(content="read me file with id 1728675498613")]}
    )
    messages = response.get("messages", [])
    assert messages != []
    assert any(
        "Gregor Mendel".lower() in message.content.lower() for message in messages
    )


def test_agent_tools_box_aks_ai():
    client: BoxClient = get_ccg_client()
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model)
    response = box_agent.chat.invoke(
        {
            "messages": [
                HumanMessage(
                    content="ask box ai to give you the key points of file 1728675498613"
                )
            ]
        }
    )
    messages = response.get("messages", [])
    assert messages != []
    assert any(
        "Gregor Mendel".lower() in message.content.lower() for message in messages
    )
