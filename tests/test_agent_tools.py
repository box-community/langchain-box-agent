from box_ai_agents_toolkit import BoxClient
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

from src.langchain_box_agent.box_agent import LangChainBoxAgent


def test_agent_tools_who_am_i(box_client_ccg: BoxClient, chat_config: str):
    client: BoxClient = box_client_ccg
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model, True)
    response = box_agent.react_agent.invoke(
        {"messages": [HumanMessage(content="who am i?")]}, chat_config
    )
    messages = response.get("messages", [])
    assert messages != []
    assert any("Authenticated" in message.content for message in messages)


def test_agent_tools_box_search(box_client_ccg: BoxClient, chat_config: str):
    client: BoxClient = box_client_ccg
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model, True)
    response = box_agent.react_agent.invoke(
        {"messages": [HumanMessage(content="locate my hab-03-01 file by name")]},
        chat_config,
    )
    messages = response.get("messages", [])
    assert messages != []
    assert any("hab-03-01" in message.content.lower() for message in messages)


def test_agent_tools_box_read_file_by_id(box_client_ccg: BoxClient, chat_config: str):
    client: BoxClient = box_client_ccg
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model, True)
    response = box_agent.react_agent.invoke(
        {"messages": [HumanMessage(content="read me file with id 1728675498613")]},
        chat_config,
    )
    messages = response.get("messages", [])
    assert messages != []
    assert any(
        "Gregor Mendel".lower() in message.content.lower() for message in messages
    )


def test_agent_tools_box_aks_ai(box_client_ccg: BoxClient, chat_config: str):
    client: BoxClient = box_client_ccg
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model, True)
    response = box_agent.react_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="ask box ai to give you the key points of file 1728675498613"
                )
            ]
        },
        chat_config,
    )
    messages = response.get("messages", [])
    assert messages != []
    assert any(
        "Gregor Mendel".lower() in message.content.lower() for message in messages
    )


def test_agent_tools_locate_folder_by_name(box_client_ccg: BoxClient, chat_config: str):
    client: BoxClient = box_client_ccg
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model, True)
    response = box_agent.react_agent.invoke(
        {"messages": [HumanMessage(content="locate folder with name hab-01")]},
        chat_config,
    )
    messages = response.get("messages", [])
    assert messages != []
    assert any(
        "298939487242".lower() in message.content.lower() for message in messages
    )


def test_agent_tools_ai_extract_date(box_client_ccg: BoxClient, chat_config: str):
    client: BoxClient = box_client_ccg
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model, True)
    response = box_agent.react_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="extract tenant name, email, contract data, and rent from file 1728675498613"
                )
            ]
        },
        chat_config,
    )
    messages = response.get("messages", [])
    assert messages != []
    assert any(
        "gregor.mendel@moonhabitat.space".lower() in message.content.lower()
        for message in messages
    )


def test_agent_tools_list_folder_content_by_folder_id(
    box_client_ccg: BoxClient, chat_config: str
):
    client: BoxClient = box_client_ccg
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(client, model, True)
    response = box_agent.react_agent.invoke(
        {"messages": [HumanMessage(content="list content of folder 298939487242")]},
        chat_config,
    )
    messages = response.get("messages", [])
    assert messages != []
    assert any(
        "HAB-1-01.docx".lower() in message.content.lower() for message in messages
    )
