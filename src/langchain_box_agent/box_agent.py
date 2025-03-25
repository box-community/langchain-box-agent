from typing import List
from langchain_core.language_models import (
    BaseChatModel,
)
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent
from langchain.tools.base import StructuredTool

from box_ai_agents_toolkit import (
    BoxClient,
    SearchForContentContentTypes,
    box_search,
    box_file_text_extract,
    box_file_ai_ask,
    box_claude_ai_agent_ask,
)
from langgraph.graph.graph import CompiledGraph


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

        self.chat = create_react_agent(model, self.tools)

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
