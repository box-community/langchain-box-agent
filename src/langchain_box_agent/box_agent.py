from langchain_core.language_models import (
    BaseChatModel,
)
from langchain.chat_models import init_chat_model


class BoxAgent:
    chat_model: BaseChatModel

    def __init__(self, model: str, model_provider: str):
        self.chat_model = init_chat_model(model, model_provider)
