import time
import uuid
from typing import Any, Iterator, Optional

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from langchain_box_agent.box_agent import LangChainBoxAgent


class SimulatedAgent:
    """Simulated Box agent that provides mock responses."""

    def __init__(self):
        """Initialize the simulated agent."""
        self.username = "RB Admin"

    def process_query(self, query: str) -> str:
        """Process a user query and return a simulated response."""
        # Simulate some processing time
        time.sleep(1)

        query_lower = query.lower()

        if "who am i" in query_lower:
            return f"You are currently authenticated as {self.username} in the Box API."

        elif "search" in query_lower and (
            "pdf" in query_lower or "file" in query_lower
        ):
            return (
                "I found the following PDF files in your Box account:\n\n"
                "- Sample PDF A.pdf (ID: 1584049890463)\n"
                "- Sample PDF B.pdf (ID: 1584052520457)\n"
                "- Open Foundation and Fine-Tuned Chat Models.pdf (ID: 1633681461006)"
            )

        elif (
            "what's in" in query_lower
            or "list" in query_lower
            or "show" in query_lower
            or "folder" in query_lower
        ):
            return (
                "Your root folder contains:\n\n"
                "Folders:\n"
                "- Habitat Leases\n"
                "- Templates\n"
                "- Movie Scripts\n\n"
                "Files:\n"
                "- Leases.csv\n"
                "- Leases.xlsx\n"
                "- sample.txt\n"
                "- Lease_Template.docx"
            )

        elif "create" in query_lower and "folder" in query_lower:
            folder_name = "LangChain Demo"
            if "called" in query_lower and query_lower.split("called")[-1].strip():
                potential_name = query_lower.split("called")[-1].strip()
                if potential_name:
                    folder_name = potential_name.strip("'\"")

            return (
                f"I've created a new folder called '{folder_name}' in your Box account."
            )

        elif "read" in query_lower and "sample.txt" in query_lower:
            return (
                "Content of sample.txt:\n\n"
                "This is a sample text file for testing Box integration with LangChain.\n"
                "You can use LangChain to build AI applications that interact with Box files and folders.\n"
                "This demo shows how to create a Box agent that can search, read, and manipulate Box files."
            )

        elif "extract" in query_lower and (
            "hab-1" in query_lower or "hab-2" in query_lower or "hab-3" in query_lower
        ):
            return (
                "Extracted data from the document:\n\n"
                "Tenant Name: John Smith\n"
                "Email: john.smith@example.com\n"
                "Contract Start Date: 2025-01-01\n"
                "Contract End Date: 2025-12-31\n"
                "Monthly Rent: $1,200"
            )

        else:
            return (
                "I understand you want to "
                + query.lower()
                + ". Could you provide more details or "
                "specify which Box operation you'd like to perform? I can help with searching, reading, "
                "creating, and listing files and folders."
            )


class RealBoxAgent:
    """Real Box agent that connects to Box API using LangChain."""

    def __init__(
        self, langchain_agent: LangChainBoxAgent, chat_id: Optional[uuid.UUID] = None
    ):
        """Initialize with a LangChain Box agent."""
        self.agent = langchain_agent
        self.chat_id: uuid.UUID = None
        self.config: dict = {}

        if chat_id is None:
            self.chat_id = uuid.uuid4()
        else:
            self.chat_id = chat_id

        self.config = {"configurable": {"thread_id": str(chat_id)}}

    def process_query(self, query: str) -> str:
        """Process a user query through the real Box agent."""
        # Call the LangChain agent
        response = self.agent.chat.invoke(
            {"messages": [HumanMessage(content=query)]}, self.config
        )
        # Extract the response content
        messages = response.get("messages", [])
        if messages:
            # Return the content of the last message
            return messages[-1].content
        else:
            return "I received an empty response from the Box API."

    def process_query_stream(self, query: str) -> Iterator[dict[str, Any] | Any]:
        """Process a user query through the real Box agent."""
        # Call the LangChain agent

        for step in self.agent.chat.stream(
            {"messages": [HumanMessage(content=query)]},
            config=self.config,
            stream_mode="values",
        ):
            message = step["messages"][-1]

            if isinstance(message, HumanMessage):
                continue

            if isinstance(message, ToolMessage):
                content = f"Using tool {message.name}"
                yield content

            if isinstance(message, AIMessage):
                content = message.content
                if content == "":
                    continue
                yield content
