# LangChain Box Agent

LangChain Box Agent is a Python library that integrates [LangChain](https://github.com/hwchase17/langchain) with the Box platform, enabling seamless interaction with Box files and folders using AI-powered tools. This project provides a set of tools and utilities to interact with Box's API, perform AI-based operations, and build intelligent workflows.

## Features

- **Box Authentication**: Supports both OAuth2.0 and Client Credentials Grant (CCG) authentication methods.
- **File Operations**: Retrieve, read, and extract text from Box files.
- **AI-Powered Tools**:
  - Ask Box AI questions about file content.
  - Extract structured data from files using AI.
- **Folder Operations**: List folder contents, locate folders by name, and perform recursive operations.
- **Search**: Search for files and folders in Box with advanced filters.
- **LangChain Integration**: Build intelligent agents using LangChain's tools and models.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/langchain-box-agent.git
   cd langchain-box-agent
   ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up environment variables: Create a .env file in the root directory with the following variables:    

    ```yaml
    BOX_CLIENT_ID=your_client_id
    BOX_CLIENT_SECRET=your_client_secret
    BOX_SUBJECT_TYPE=enterprise_or_user
    BOX_SUBJECT_ID=your_subject_id
    ```

## Usage
### Authentication
Authenticate with Box using CCG:
```python
from box_ai_agents_toolkit import (
    BoxClient,
    get_ccg_client,
)

client: BoxClient = get_ccg_client()
```

### LangChain Box Agent
Create a LangChain Box Agent to interact with Box:
```python
import uuid
from langchain.chat_models import init_chat_model
from src.langchain_box_agent.box_agent import LangChainBoxAgent

client = get_ccg_client()
model = init_chat_model("gpt-4", model_provider="openai")

chat_id = uuid.uuid4()
chat_config =  {"configurable": {"thread_id": str(chat_id)}}

box_agent = LangChainBoxAgent(client, model)

response = box_agent.chat.invoke(
        {"messages": [HumanMessage(content="hello world")]}, chat_config
    )

print(response)
```

## Tools
- Who Am I: Check the current authenticated user.
- Search: Search for files or folders in Box.
- Read File: Extract text content from a file.
- Ask AI: Ask Box AI questions about file content.
- Extract Data: Extract structured data from files using AI.
- List Folder Content: List the contents of a folder.


## Running the demo
Make sure TKInter is installed in your system.

For MacOS:
```bash
brew install python-tk
```

And then run the demo:
```bash
uv run src/run_agent_demo.py
```

## Development
### Running Tests

Run the test suite using `pytest`:

```bash
uv run pytest
```
### Code Style
This project uses Ruff for linting. Run the following command to check for linting issues:

### Adding Dependencies
Add new dependencies to the pyproject.toml file under the appropriate section.

### Contributing
Contributions are welcome! 

License
This project is licensed under the MIT License. See the LICENSE file for details.

