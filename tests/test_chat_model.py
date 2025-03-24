from src.langchain_box_agent.box_agent import LangChainBoxAgent
from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model


def test_box_agent_chat_model_simple():
    model = init_chat_model("gpt-4", model_provider="openai")
    box_agent = LangChainBoxAgent(model)

    response = box_agent.chat_model.invoke([HumanMessage(content="hi!")])

    assert response.content is not None
    assert len(response.content) >= 1
