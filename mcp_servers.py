from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack

from tools import TOOL_SCHEMAS, TOOLS as LOCAL_TOOLS

MCP_SERVERS = {
    "time": StdioServerParameters(
        command="uvx",
        args=["mcp-server-time"],
    ),
    "fetch": StdioServerParameters(
        command="uvx",
        args=["mcp-server-fetch"],
    ),
}

mcp_sessions:  dict[str, ClientSession] = {}

async def connect_mcp(stack: AsyncExitStack):
    """Launch each MCP server and merge its tools into TOOL_SCHEMAS"""
    for name, params in MCP_SERVERS.items():
        read, write = await stack.enter_async_context(stdio_client(params))
        session = await stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        
        tools = (await session.list_tools()).tools
        for tool in tools:
            mcp_sessions[tool.name] = session
            TOOL_SCHEMAS.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema,
                }
            })
        print(f" - [mcp] connected '{name}' with {len(tools)} tools", [tool.name for tool in tools])
        
async def call_tool(name: str, args: dict) -> str:
    """Run a tool - ours directly, or an MCP server's over the protocol."""
    if name in LOCAL_TOOLS:
        return LOCAL_TOOLS[name](**args)
    if name not in mcp_sessions:
        return f"Error: no tool named {name}"
    result = await mcp_sessions[name].call_tool(name, args)
    return "\n".join(c.text for c in result.content if hasattr(c, 'text'))