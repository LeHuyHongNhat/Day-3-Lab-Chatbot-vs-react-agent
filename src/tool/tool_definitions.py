"""
Tool definitions for the ReAct Agent.
Each tool should have: name, description, and a callable function.
"""

from src.tool.reader import clean_text, extract_abstract, extract_metadata
from typing import Dict, Any

# Tool registry - maps tool names to their implementations
TOOL_REGISTRY = {
    "clean_text": clean_text,
    "extract_abstract": extract_abstract,
    "extract_metadata": extract_metadata,
}

# Tool definitions for the agent
def get_available_tools() -> list:
    """
    Returns a list of available tools with their descriptions.
    Format expected by ReActAgent.
    """
    return [
        {
            "name": "clean_text",
            "description": "Clean text by removing strange characters, normalizing unicode, and fixing whitespace. Input: text (str). Returns: cleaned text (str).",
            "callable": clean_text,
        },
        {
            "name": "extract_abstract",
            "description": "Extract abstract from research paper or long text. Looks for 'Abstract' section or extracts first paragraph. Input: text (str), max_sentences (int, optional). Returns: abstract (str).",
            "callable": extract_abstract,
        },
        {
            "name": "extract_metadata",
            "description": "Extract metadata from text including title, abstract, word count. Input: text (str). Returns: dictionary with metadata.",
            "callable": extract_metadata,
        },
    ]


def execute_tool(tool_name: str, **kwargs) -> Any:
    """
    Execute a tool by name with given arguments.

    Args:
        tool_name: Name of the tool to execute
        **kwargs: Arguments to pass to the tool

    Returns:
        Result from the tool execution
    """
    if tool_name not in TOOL_REGISTRY:
        return f"Error: Tool '{tool_name}' not found. Available tools: {list(TOOL_REGISTRY.keys())}"

    try:
        tool_func = TOOL_REGISTRY[tool_name]
        return tool_func(**kwargs)
    except TypeError as e:
        return f"Error executing {tool_name}: Invalid arguments. {str(e)}"
    except Exception as e:
        return f"Error executing {tool_name}: {str(e)}"