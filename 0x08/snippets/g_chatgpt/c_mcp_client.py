# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet demonstrates an MCP client using Anthropic's API
to interact with an MCP server.

Teaching focus
  - Anthropic API with MCP server integration
  - mcp_servers parameter in messages.create

Preparations
  - .env file with credentials, not part of the project; entries e.g.,
        ANTHROPIC_API_KEY=xyz
  - virtual environment activated and libs installed, here:
        pip install anthropic python-dotenv
  - MCP server (b_mcp_server.py) must be running on localhost:8000

See
  - https://console.anthropic.com/dashboard
"""

import os
from dotenv import load_dotenv

from anthropic import Anthropic

load_dotenv()                               # load from .env


def chat():
    """ chat with Anthropic using MCP server tools """
    client = Anthropic(
        api_key=os.environ['ANTHROPIC_API_KEY'],  # this is also the default, it can be omitted
    )
    print(f"api key {client.api_key}")
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",  # or claude-3-sonnet, claude-3-haiku
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Please call greet://Alice and add 7 and 9 using your tools."}
        ],
        mcp_servers=[
            {"name": "DemoServer", "url": "http://localhost:8000"}
        ]
    )

    print(response.content[0].text)


if __name__ == "__main__":
    chat()
