# (C) A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

"""
This snippet demonstrates an MCP (Model Context Protocol) server
using FastMCP with calculator tools and resources.

Teaching focus
  - MCP server setup with FastMCP
  - defining tools (@mcp.tool)
  - defining resources (@mcp.resource)
  - streamable-http transport

Preparations
  - virtual environment activated and libs installed, here:
        pip install mcp
"""

import sys
import platform

print(f'moin moin - 7 - {platform.python_version()}', file=sys.stderr)

from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Simple Calculator Server")


@mcp.tool()
def add_numbers(a: float, b: float) -> dict:
    """Add two numbers together"""
    result = a + b
    return {
        "result": result,
        "operation": f"{a} + {b} = {result}"
    }


@mcp.tool()
def multiply_numbers(a: float, b: float) -> dict:
    """Multiply two numbers"""
    result = a * b
    return {
        "result": result,
        "operation": f"{a} × {b} = {result}"
    }


@mcp.tool()
def calculate_power(base: float, exponent: float) -> dict:
    """Calculate base raised to the power of exponent"""
    result = base ** exponent
    return {
        "result": result,
        "operation": f"{base}^{exponent} = {result}"
    }


# Fix the resource URI format - use proper URI scheme
@mcp.resource("calculator://server-info")
def get_server_info() -> str:
    """Get information about this calculator server"""
    return """
    Calculator MCP Server
    ====================

    Available Tools:
    - add_numbers(a, b): Add two numbers
    - multiply_numbers(a, b): Multiply two numbers
    - calculate_power(base, exponent): Calculate power

    Available Resources:
    - calculator://server-info: This information
    - calculator://help: Help documentation
    """


@mcp.resource("calculator://help")
def get_help() -> str:
    """Get help documentation"""
    return """
    Calculator Help
    ===============

    This is a simple calculator MCP server that provides basic mathematical operations.

    Usage:
    - Use the tools to perform calculations
    - Access resources for server information and help
    """


if __name__ == "__main__":
    #mcp.run()
    mcp.run(transport="streamable-http")
