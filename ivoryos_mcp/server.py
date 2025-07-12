# server.py
import os
from typing import Optional

from mcp.server.fastmcp import FastMCP
import httpx
from dotenv import load_dotenv
from ivoryos_client import IvoryosClient



# Initialize the client
load_dotenv()
ivoryos_client = IvoryosClient(
    url=os.getenv("IVORYOS_URL", "http://127.0.0.1:8000/ivoryos"),
    username=os.getenv("IVORYOS_USERNAME", "admin"),
    password=os.getenv("IVORYOS_PASSWORD", "admin")
)

# Create MCP server
mcp = FastMCP("IvoryOS MCP")


def main():
    mcp.run()


# MCP Tool wrappers - now much cleaner!
@mcp.tool("platform-info")
def summarize_deck_function() -> str:
    """summarize ivoryOS and the current deck functions, no authentication required."""
    return ivoryos_client.get_platform_info()


@mcp.tool("execution-status")
def execution_status():
    """Get workflow status"""
    try:
        return ivoryos_client.get_execution_status()
    except Exception as e:
        return f"Error getting workflow status: {str(e)}"


@mcp.tool("execute-task")
def execute_task(component: str, method: str, kwargs: dict = None) -> str:
    """Execute a robot task and return task_id."""
    try:
        result = ivoryos_client.execute_task(component, method, kwargs)
        return f"{result}. Use `execution-status` to monitor."
    except Exception as e:
        return f"Error executing task: {str(e)}"


@mcp.tool("list-workflow-scripts")
def list_workflow_script(search_key: str = '', deck_name: str = '') -> str:
    """List workflow scripts"""
    try:
        return ivoryos_client.list_workflow_scripts(search_key, deck_name)
    except Exception as e:
        return f"Error listing workflow scripts: {str(e)}"


@mcp.tool("load-workflow-script")
def load_workflow_script(workflow_name: str) -> str:
    """Load a workflow script"""
    try:
        return ivoryos_client.load_workflow_script(workflow_name)
    except Exception as e:
        return f"Error loading workflow script: {str(e)}"


@mcp.tool("submit-workflow-script")
def submit_workflow_script(workflow_name: str, main_script: str = "",
                           cleanup_script: str = "", prep_script: str = "") -> str:
    """Submit a workflow script"""
    try:
        return ivoryos_client.submit_workflow_script(workflow_name, main_script, cleanup_script, prep_script)
    except Exception as e:
        return f"Error submitting workflow script: {str(e)}"


@mcp.tool("pause-and-resume")
def pause_and_resume() -> str:
    """Toggle pause and resume for workflow execution"""
    try:
        return ivoryos_client.pause_and_resume()
    except Exception as e:
        return f"Error toggling workflow pause/resume: {str(e)}"


@mcp.tool("abort-pending-workflow")
def abort_pending_workflow_iterations() -> str:
    """Abort pending workflow execution"""
    try:
        return ivoryos_client.abort_pending_workflow()
    except Exception as e:
        return f"Error aborting pending workflow: {str(e)}"


@mcp.tool("stop-current-workflow")
def stop_workflow() -> str:
    """Stop workflow execution after current step"""
    try:
        return ivoryos_client.stop_current_workflow()
    except Exception as e:
        return f"Error stopping current workflow: {str(e)}"


@mcp.tool("run-workflow-repeat")
def run_workflow(repeat_time: Optional[int] = None) -> str:
    """Run the loaded workflow with repeat times"""
    try:
        return ivoryos_client.run_workflow_repeat(repeat_time)
    except Exception as e:
        return f"Error starting workflow execution: {str(e)}"


@mcp.tool("run-workflow-kwargs")
def run_workflow_with_kwargs(kwargs_list: list[dict] = None) -> str:
    """Run the loaded workflow with a list of keyword arguments"""
    try:
        return ivoryos_client.run_workflow_kwargs(kwargs_list)
    except Exception as e:
        return f"Error starting workflow execution: {str(e)}"


@mcp.tool("run-workflow-campaign")
def run_workflow_campaign(parameters: list[dict], objectives: list[dict],
                          repeat: int = 25, parameter_constraints: list[str] = []) -> str:
    """Run the loaded workflow with ax-platform (credit: Honegumi)"""
    try:
        return ivoryos_client.run_workflow_campaign(parameters, objectives, repeat, parameter_constraints)
    except Exception as e:
        return f"Error starting workflow execution: {str(e)}"


@mcp.tool("list-workflow-data")
def list_workflow_data(workflow_name: str = "") -> str:
    """List workflow data"""
    try:
        return ivoryos_client.list_workflow_data(workflow_name)
    except Exception as e:
        return f"Error listing workflow data: {str(e)}"


@mcp.tool("load-workflow-data")
def load_workflow_data(workflow_id: int) -> str:
    """Load workflow data"""
    try:
        return ivoryos_client.load_workflow_data(workflow_id)
    except Exception as e:
        return f"Error loading workflow data: {str(e)}"


# Prompts remain the same
@mcp.prompt("generate-workflow-script")
def generate_custom_script() -> str:
    """Prompt for writing workflow script. No authentication required"""
    return """
    find the most appropriate function based on the task description
    ,and write them into a Python function without need to import the deck. 
    And write only needed return values as dict
    ```
    def workflow_static():
        if True:
            results = deck.sdl.analyze(**{'param_1': 1, 'param_2': 2})
        time.sleep(1.0)
        return {'results':results,}
    ```
    or
    ```
    def workflow_dynamic(param_1, param_2):
        if True:
            results = deck.sdl.analyze(**{'param_1': param_1, 'param_1': param_2})
        time.sleep(1.0)
        return {'results':results,}
    ```
    Please only use these available action names.
    """


@mcp.prompt("campaign-design")
def ax_campaign_design() -> str:
    """Prompt for writing workflow campaign. No authentication required (template credit: Honegumi)"""
    return """
    these are examples code of creating parameters, objectives and constraints
    parameters=[
        {"name": "x1", "type": "range", "value": 10.0},
        {"name": "x2", "type": "fixed", "bounds": [0.0, 10.0]},
        {
            "name": "c1",
            "type": "choice",
            "is_ordered": False,
            "values": ["A", "B", "C"],
        },
    ]
    objectives=[
        {"name": "obj_1", "minimize": True},
        {"name": "obj_2", "minimize": False},
    ]
    parameter_constraints=[
        "x1 + x2 <= 15.0",  # example of a sum constraint, which may be redundant/unintended if composition_constraint is also selected
        "x1 + x2 <= {total}",  # reparameterized compositional constraint, which is a type of sum constraint
        "x1 <= x2",  # example of an order constraint
        "1.0*x1 + 0.5*x2 <= 15.0",  # example of a linear constraint. Note the lack of space around the asterisks
    ],
    """


if __name__ == "__main__":
    print("Running...")
    main()