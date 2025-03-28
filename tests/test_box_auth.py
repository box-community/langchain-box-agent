from box_sdk_gen import BoxClient, User
from dotenv import load_dotenv

load_dotenv()


def test_get_ccg_client(box_client_ccg: BoxClient):
    client = box_client_ccg
    me: User = client.users.get_user_me()

    assert me.id is not None
    assert me.type == "user" or me.type == "enterprise"
    assert me.name is not None
    assert me.login is not None
