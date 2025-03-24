from langchain_core.language_models import (
    BaseChatModel,
)
from langchain.chat_models import init_chat_model


class BoxAgent:
    chat_model: BaseChatModel

    def __init__(self, chat_model: BaseChatModel):
        self.chat_model = chat_model
