from fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location:str)->str:
    """주어진 위치의 날씨를 리턴합니다."""
    return f"{location}의 오늘 날씨는 맑습니다."

if __name__ == '__main__':
    mcp.run(transport='sse')