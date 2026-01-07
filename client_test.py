import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    # Most of this file is this file from MCP PythonSDK's github:
    # https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/streamable_basic.py
    
    # Connect to MCP streamable HTTP server
    async with streamable_http_client("http://127.0.0.1:8000/mcp") as (read_stream, write_stream, _):
        # Create a client session 
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Confirming connection by listing the tools
            tools_response = await session.list_tools()
            
            # Print out the tools we can use (mostly for testing)
            print("Available tools:", [t.name for t in tools_response.tools])

            # Call the one of the available tools
            result = await session.call_tool(
                name='calculate_betting_odds',
                arguments={"fighter1_name": "Conor McGregor", "fighter2_name": "Dustin Poirier"}
            )

            # result = await session.call_tool(
            #     name='fighter_summary',
            #     arguments={"fighter_name": "Conor McGregor"}
            # )

            # CallToolResult objects have structured content attributes
            print("Result:", result.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
