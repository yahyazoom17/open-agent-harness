import sys
from memory import load_memory
from tools import TOOL_SCHEMAS

def handle_command(line: str) -> bool:
    if not line.startswith("/"):
        return False
    cmd, _, arg = line.partition(" ")
    if cmd == "/models":
        print("\nAvailable models:\n")
        print(" - llama3.2:1b (ollama)")
        print(" - nvidia/nemotron-3-super-120b-a12b:free (openrouter)")
        return True
    elif cmd == "/tools":
        print("\nAvailable tools:\n")
        for tool in TOOL_SCHEMAS:
            print(f" - {tool['function']['name']}: {tool['function']['description']}")
        return True    
    elif cmd == "/memory":
        memory = load_memory()
        if not memory:
            print("\nAgent Memory is empty.")
        else:
            print("\nAgent Memory contents:")
            print(memory)
        return True        
    if cmd == "/exit":
        print("Exiting...")
        sys.exit()
    elif cmd == "/help":
        print("\nAvailable commands:")
        print("/models - List available models")
        print("/memory - Show the agent's memory")
        print("/exit - Exit the program")
        print("/help - Show this help message")
        return True
    return False