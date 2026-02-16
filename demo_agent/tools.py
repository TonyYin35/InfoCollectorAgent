from langchain_core.tools import tool
from datetime import datetime


@tool
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def calculate(expression: str) -> str:
    """Evaluate a math expression. Example: '2 + 3 * 4'"""
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expression):
        return "Error: only numeric math expressions are allowed."
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"


@tool
def search_info(query: str) -> str:
    """Search for information (mock). Returns a placeholder response."""
    return (
        f"[Mock search result for '{query}']: "
        "This is a placeholder. Replace this tool with a real search API "
        "(e.g. Tavily, SerpAPI) for actual results."
    )


ALL_TOOLS = [get_current_time, calculate, search_info]
