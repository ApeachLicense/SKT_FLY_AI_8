from fastmcp import FastMCP
import os

mcp = FastMCP("Math")

@mcp.tool()
def add(a:int, b:int) -> int :
    """Add two number"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two number """
    return a * b

if __name__ == "__main__":
    mcp.run(transport = "stdio")