# client.py
import asyncio
from fastmcp import Client

async def main():
    # point to the full MCP path
    async with Client("http://127.0.0.1:8000/mcp/") as client:
        await client.ping()                # sanity check
        print("tools:", await client.list_tools())

asyncio.run(main())
