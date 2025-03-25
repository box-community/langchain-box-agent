from langchain_core.tools import tool

from box_ai_agents_toolkit import BoxClient, get_ccg_client


@tool(parse_docstring=True)
def box_who_am_i() -> str:
    """who am I, Retrieves the current user's information in box. Checks the connection to Box

    Returns:
        str: A string containing the current user's information.
    """
    client: BoxClient = get_ccg_client()
    # Get the current user's information
    current_user = client.users.get_user_me()

    return f"Authenticated as: {current_user.name}"
