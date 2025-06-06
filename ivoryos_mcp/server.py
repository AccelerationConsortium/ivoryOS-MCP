# server.py
from mcp.server.fastmcp import FastMCP
import httpx


# Create an MCP server
mcp = FastMCP("IvoryOS MCP")

# IvoryOS url
url = "http://127.0.0.1:8000/ivoryos"


@mcp.tool("deck-info")
def summarize_deck_function() -> str:
    """summarize the current deck functions"""
    try:
        snapshot = httpx.get(f"{url}/backend_control").json()
        return f"summarize the python function representation {snapshot}"
    except Exception:
        return "there is not deck available."

# @mcp.tool("submit-script")
# def submit_script(script:str) -> str:
#     """summarize the current deck functions"""
#     try:
#         snapshot = httpx.post(f"{url}/submit_script", data={"script":script})
#         return f"submitted"
#     except Exception:
#         return "there is not deck available."

# Add a dynamic greeting resource
@mcp.resource("functions://{component}")
def get_component_functions(component: str) -> str:
    """Get a personalized greeting"""
    try:
        snapshot = httpx.get(f"{url}/backend_control").json()
        if component in snapshot.keys():
            return f"the function signature is {snapshot[component]}"
        return f"This component is not available on current deck, please use {snapshot.keys()}"
    except Exception:
        return "there is not deck available."


@mcp.prompt()
def generate_custom_script() -> str:
    """summarize the current deck functions"""
    try:
        snapshot = httpx.get(f"{url}/backend_control").json()
        return f"""
                These are my functions signatures,
                {snapshot}
                and I want you to find the most appropriate function based on the task description
                ,and write them into a Python function. Please only use these available action names 
                from above 
                """
    except Exception:
        return "there is not deck available."
