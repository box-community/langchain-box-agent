import uuid
from typing import Any, Iterator, Optional

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from langchain_box_agent.box_agent import LangChainBoxAgent


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
        response = self.agent.react_agent.invoke(
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

        for step in self.agent.react_agent.stream(
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
