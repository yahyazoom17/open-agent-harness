from pathlib import Path

MEMORY_FILE = Path(__file__).parent / "MEMORY.md"

def load_memory():
    """Load the agent memory from the MEMORY.md file."""
    if MEMORY_FILE.is_file():
        return MEMORY_FILE.read_text(encoding="utf-8")
    return "(nothing saved in memory yet)"

def save_memory(memory: str):
    """Save the agent memory to the MEMORY.md file."""
    with MEMORY_FILE.open("a", encoding="utf-8") as f:
        f.write(f"- {memory}\n")
    return f" - [memory] saved {memory} to agent memory"