import os
import asyncio
import sys
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

# load api key
load_dotenv(override=True)
print(os.getenv('OPENAI_API_KEY')[:30])

async def main():
    # mcp server 설정
    client = MultiServerMCPClient(
        {
            # 'math': {
            #     'transport': 'stdio', 
            #     'command': sys.executable, 
            #     'args': [r'C:\Users\jwkim\Desktop\agent\10_mcp\math_server.py']
            # }, 
            # 'weather': {
            #     'transport': 'sse', 
            #     'url': 'http://localhost:8000/sse'
            # },
            # "filesystem": {
            #     "command": "npx.cmd",
            #     "args": [ "-y", "@modelcontextprotocol/server-filesystem", "C:\\temp" ]
            # },
            "airbnb_mcp":{
                "transport": "stdio",
                "command": "npx.cmd",
                "args": ["-y","@openbnb/mcp-server-airbnb", "--ignore-robots-txt"]
            }
        }
    )

    tools = await client.get_tools()
    llm = init_chat_model("gpt-4o", temperature=0)
    agent = create_agent(
        model=llm, 
        tools=tools,
        system_prompt='사용자의 요청에 반드시 도구를 사용 하세요.', 
    )

    user_input = {
        "messages":[
            ("user","스탬포드 브릿지 근처 호텔을 추천해줘.")
        ]
    }

    response = await agent.ainvoke(user_input)
    print(response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())