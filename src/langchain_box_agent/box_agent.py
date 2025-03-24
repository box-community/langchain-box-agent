from langchain_core.language_models import (
    BaseChatModel,
)


class LangChainBoxAgent:
    chat_model: BaseChatModel

    def __init__(self, chat_model: BaseChatModel):
        self.chat_model = chat_model
