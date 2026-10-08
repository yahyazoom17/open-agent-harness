from dotenv import load_dotenv
load_dotenv()
import json
import sys
import asyncio
from contextlib import AsyncExitStack
from config import LLM_PROVIDER, LLM_MODEL, AGENT_SYSTEM_PROMPT
from utils import configure_llm_client
from tools import TOOL_SCHEMAS, TOOLS
from mcp_servers import connect_mcp
from command import handle_command

sys.stdout.reconfigure(encoding='utf-8')

client = configure_llm_client()

async def run_agent(user_messages:str) -> str:    
    
    messages = [
        {"role": "system", "content": AGENT_SYSTEM_PROMPT.format(memory=TOOLS["load_memory"]())},
        {"role": "user", "content": user_messages},
    ]    
    
    while True:    
        response = await client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )
        
        message = response.choices[0].message
        
        if not message.tool_calls:
            return message.content or ""    
            
        messages.append(message)
        
        for call in message.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            print(f" - [tool] {call.function.name}({args})")
            result = TOOLS[call.function.name](**args)
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

async def main():
    async with AsyncExitStack() as stack:
        await connect_mcp(stack)
        print(f"Agent Harness (using {LLM_MODEL} with {len(TOOL_SCHEMAS)} tools) - CTRL+C to exit")
        try:
            while True:
                line = (await asyncio.to_thread(input, "\nYou: ")).strip()
                if not line or handle_command(line):
                    continue
                print("\nAgent:", await run_agent(line))
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")

if __name__ == "__main__":
    asyncio.run(main())