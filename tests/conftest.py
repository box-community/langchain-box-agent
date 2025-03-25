import pytest
from box_sdk_gen import BoxClient

from src.langchain_box_agent.box.box_authentication import (
    get_ccg_client,
    # get_oauth_client,
)

# @pytest.fixture
# def box_client_auth() -> BoxClient:
#     return get_oauth_client()


@pytest.fixture
def box_client_ccg() -> BoxClient:
    return get_ccg_client()
