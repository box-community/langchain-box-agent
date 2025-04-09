import uuid

import pytest
from box_ai_agents_toolkit import (
    BoxClient,
    get_ccg_client,
)

# @pytest.fixture
# def box_client_auth() -> BoxClient:
#     return get_oauth_client()


@pytest.fixture
def chat_config() -> str:
    chat_id = uuid.uuid4()
    return {"configurable": {"thread_id": str(chat_id)}}


@pytest.fixture
def box_client_ccg() -> BoxClient:
    return get_ccg_client()
