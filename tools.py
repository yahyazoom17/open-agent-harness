from pathlib import Path

WORKSPACE = Path(__file__).parent / "workspace"

def list_files() -> str:
    """List all files in assistant workspace directory."""
    return "\n".join(p.name for p in WORKSPACE.iterdir()) or "(empty)"

def read_file(file_name: str) -> str:
    """Read a file from the assistant workspace directory."""
    file_path = WORKSPACE / file_name
    if not file_path.is_file():
        return f"Error: no file named {file_name}"
    return file_path.read_text(encoding="utf-8")

def write_file(file_name: str, content: str) -> str:
    """Write/overwrite a file to the assistant workspace directory."""
    file_path = WORKSPACE / file_name
    file_path.write_text(content, encoding="utf-8")
    return f"Wrote {len(content)} bytes to {file_name}"

TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files in the user's workspace directory.",
            "parameters": {
                "type": "object",
                "properties": {},
            }            
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file from the user's workspace directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The name of the file to read.",
                    }
                },
                "required": ["file_name"],
            }            
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write/overwrite a file to the user's workspace directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "The name of the file to write.",
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file.",
                    }
                },
                "required": ["file_name", "content"],
            }            
        }
    },
]