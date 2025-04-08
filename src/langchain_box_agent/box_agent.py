import json
from typing import List, Union

from box_ai_agents_toolkit import (
    BoxClient,
    File,
    Folder,
    SearchForContentContentTypes,
    box_claude_ai_agent_ask,
    box_claude_ai_agent_extract,
    box_file_ai_ask,
    box_file_ai_extract,
    box_file_text_extract,
    box_folder_list_content,
    box_locate_folder_by_name,
    box_search,
)
from langchain.tools.base import StructuredTool
from langchain_core.language_models import (
    BaseChatModel,
)
from langchain_core.tools import BaseTool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent


class LangChainBoxAgent:
    client: BoxClient
    chat: CompiledGraph
    # chat_model: BaseChatModel
    tools: List[BaseTool] = []
    # agent = CompiledGraph

    def __init__(self, client: BoxClient, model: BaseChatModel):
        # self.chat_model = chat_model
        self.client = client
        self.tools.append(
            StructuredTool.from_function(
                self.box_who_am_i,
                parse_docstring=True,
            )
        )
        self.tools.append(
            StructuredTool.from_function(
                self.box_search_tool,
                parse_docstring=True,
            )
        )
        self.tools.append(
            StructuredTool.from_function(
                self.box_read_tool,
                parse_docstring=True,
            )
        )
        self.tools.append(
            StructuredTool.from_function(
                self.box_ask_ai_tool,
                parse_docstring=True,
            )
        )
        self.tools.append(
            StructuredTool.from_function(
                self.box_search_folder_by_name,
                parse_docstring=True,
            )
        )
        self.tools.append(
            StructuredTool.from_function(
                self.box_ai_extract_data,
                parse_docstring=True,
            )
        )
        self.tools.append(
            StructuredTool.from_function(
                self.box_list_folder_content_by_folder_id,
                parse_docstring=True,
            )
        )

        memory = MemorySaver()

        self.chat = create_react_agent(model, self.tools, checkpointer=memory)

        # chat_model.bind_tools(self.tools)

    def box_who_am_i(self) -> str:
        """who am I, Retrieves the current user's information in box. Checks the connection to Box

        Returns:
            str: A string containing the current user's information.
        """
        current_user = self.client.users.get_user_me()

        return f"Authenticated as: {current_user.name}"

    def box_search_tool(
        self,
        query: str,
        file_extensions: List[str] | None = None,
        where_to_look_for_query: List[str] | None = None,
        ancestor_folder_ids: List[str] | None = None,
    ) -> str:
        """Searches for files in Box using the specified query and filters.

        Args:
            query (str): The search query.
            file_extensions (List[str] | None): A list of file extensions to filter results (e.g., ['.pdf']).
            where_to_look_for_query (List[str] | None): Specifies where to search for the query. Possible values:
                NAME
                DESCRIPTION
                FILE_CONTENT
                COMMENTS
                TAG
            ancestor_folder_ids (List[str] | None): A list of ancestor folder IDs to limit the search scope.

        Returns:
            str: A formatted string containing the search results.
        """

        # Convert the where to look for query to content types
        content_types: List[SearchForContentContentTypes] = []
        if where_to_look_for_query:
            for content_type in where_to_look_for_query:
                content_types.append(SearchForContentContentTypes[content_type])

        # Search for files with the query
        search_results = box_search(
            self.client, query, file_extensions, content_types, ancestor_folder_ids
        )

        # Return the "id", "name", "description" of the search results
        search_results = [
            f"{file.name} (id:{file.id})"
            + (f" {file.description}" if file.description else "")
            for file in search_results
        ]

        return "\n".join(search_results)

    def box_read_tool(self, file_id: str) -> str:
        """Reads the text content of a file in Box.

        Args:
            file_id (str): The ID of the file to read.

        Returns:
            str: The text content of the file.
        """
        response = box_file_text_extract(self.client, file_id)
        return response

    def box_ask_ai_tool(self, file_id: str, prompt: str) -> str:
        """Asks Box AI about a file in Box.

        Args:
            file_id (str): The ID of the file to analyze.
            prompt (str): The prompt or question to ask the AI.

        Returns:
            str: The AI-generated response based on the file's content.
        """
        ai_agent = box_claude_ai_agent_ask()
        response = box_file_ai_ask(
            self.client, file_id, prompt=prompt, ai_agent=ai_agent
        )

        return response

    def box_search_folder_by_name(self, folder_name: str) -> str:
        """Locates a folder in Box by its name.

        Args:
            folder_name (str): The name of the folder to locate.

        Returns:
            str: A formatted string containing the folder's ID and name.
        """

        search_results = box_locate_folder_by_name(self.client, folder_name)

        # Return the "id", "name", "description" of the search results
        search_results = [
            f"{folder.name} (id:{folder.id})" for folder in search_results
        ]

        return "\n".join(search_results)

    def box_ai_extract_data(self, file_id: str, fields: str) -> str:
        """Extracts data from a file in Box using AI.

        Args:
            file_id (str): The ID of the file to analyze.
            fields (str): The fields to extract from the file.

        Returns:
            str: The extracted data in JSON string format.
        """

        ai_agent = box_claude_ai_agent_extract()
        response = box_file_ai_extract(self.client, file_id, fields, ai_agent=ai_agent)

        return json.dumps(response)

    def box_list_folder_content_by_folder_id(
        self, folder_id: str, is_recursive: bool
    ) -> str:
        """Lists the content of a folder in Box by its ID.

        Args:
            folder_id (str): The ID of the folder to list the content of.
            is_recursive (bool): Whether to list the content recursively.

        Returns:
            str: The content of the folder in JSON string format, including the "id", "name", "type", and "description".
        """

        response: List[Union[File, Folder]] = box_folder_list_content(
            self.client, folder_id, is_recursive
        )

        response = [
            {
                "id": item.id,
                "name": item.name,
                "type": item.type,
                "description": item.description
                if hasattr(item, "description")
                else None,
            }
            for item in response
        ]
        return json.dumps(response)
