from box_ai_agents_toolkit import BoxClient, get_ccg_client
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from src.langchain_box_agent.box_agent import LangChainBoxAgent
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


def test_agent_tools_locate_folder_by_name():
    client: BoxClient = get_ccg_client()
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model)
    response = box_agent.chat.invoke(
        {"messages": [HumanMessage(content="locate folder with name hab-01")]}
    )
    messages = response.get("messages", [])
    assert messages != []
    assert any(
        "298939487242".lower() in message.content.lower() for message in messages
    )


def test_agent_tools_ai_extract_date():
    client: BoxClient = get_ccg_client()
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model)
    response = box_agent.chat.invoke(
        {
            "messages": [
                HumanMessage(
                    content="extract tenant name, email, contract data, and rent from file 1728675498613"
                )
            ]
        }
    )
    messages = response.get("messages", [])
    assert messages != []
    assert any(
        "gregor.mendel@moonhabitat.space".lower() in message.content.lower()
        for message in messages
    )


def test_agent_tools_list_folder_content_by_folder_id():
    client: BoxClient = get_ccg_client()
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model)
    response = box_agent.chat.invoke(
        {"messages": [HumanMessage(content="list content of folder 298939487242")]}
    )
    messages = response.get("messages", [])
    assert messages != []
    assert any(
        "HAB-1-01.docx".lower() in message.content.lower() for message in messages
    )
