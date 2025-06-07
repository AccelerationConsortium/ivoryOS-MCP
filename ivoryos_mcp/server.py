# server.py
from mcp.server.fastmcp import FastMCP
import httpx


# Create an MCP server
mcp = FastMCP("IvoryOS MCP")

# IvoryOS url
url = "http://127.0.0.1:8000/ivoryos"
login_data = {
    "username": "admin",
    "password": "admin"
}
client = httpx.Client(follow_redirects=True)


def _check_authentication():
    global client
    try:
        resp = client.get(f"{url}/", follow_redirects=False)
        if resp.status_code == httpx.codes.OK:
            return True
        else:
            login_resp = client.post(f"{url}/login", data=login_data)
            return login_resp.status_code == 200
    except httpx.ConnectError:
        return False


@mcp.tool("deck-info")
def summarize_deck_function() -> str:
    """summarize the current deck functions"""
    try:
        snapshot = client.get(f"{url}/backend_control").json()
        return f"summarize the python function representation {snapshot}"
    except Exception:
        return "there is not deck available."


# Add a dynamic greeting resource
@mcp.resource("functions://{component}")
def get_component_functions(component: str) -> str:
    """Get a personalized greeting"""
    try:
        snapshot = client.get(f"{url}/backend_control").json()
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
                ,and write them into a Python function without need to import the deck. And write return values
                as dict
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
                Please only use these available action names from above 
                """
    except Exception:
        return "there is not deck available."



@mcp.tool("pause_and_resume")
def pause_and_resume() -> str:
    """toggle pause and resume for workflow execution"""
    if not _check_authentication():
        return f"Having issues logging in to ivoryOS."
    msg = client.post(f"{url}/api/pause").json()
    return msg



@mcp.tool("abort_pending_workflow_iterations")
def abort_pending_workflow_iterations() -> str:
    """abort pending workflow execution"""
    if not _check_authentication():
        return f"Having issues logging in to ivoryOS, or ivoryOS server is not running."
    msg = client.post(f"{url}/api/abort_pending").json()
    return msg

@mcp.tool("stop_current_workflow")
def stop_workflow() -> str:
    """stop workflow execution after current step"""
    if not _check_authentication():
        return f"Having issues logging in to ivoryOS, or ivoryOS server is not running."
    msg = client.post(f"{url}/api/abort_current").json()
    return msg


@mcp.tool("repeat_run_workflow")
def repeat_run_workflow(repeat_time: int = None) -> str:
    """stop workflow execution after current step"""
    if not _check_authentication():
        return f"Having issues logging in to ivoryOS, or ivoryOS server is not running."
    client.post(f"{url}/experiment", data={"repeat": str(repeat_time)})
    return "workflow execution started."


@mcp.tool("run_workflow_with_parameters")
def run_workflow_with_kwargs(kwargs_list: list[dict] = None) -> str | int:
    """stop workflow execution after current step"""
    if not _check_authentication():
        return f"Having issues logging in to ivoryOS, or ivoryOS server is not running."

    kwargs_to_ivoryos_format = {}
    for index, kwargs in enumerate(kwargs_list):
        for key, value in kwargs.items():
            kwargs_to_ivoryos_format[f"{key}[{index+1}]"] = value
    kwargs_to_ivoryos_format["online-config"] = ""
    response = client.post(f"{url}/experiment", data=kwargs_to_ivoryos_format)
    return response.status_code


@mcp.tool("load_workflow_script")
def load_workflow_script(workflow_name:str) -> str:
    """get current workflow script"""
    if not _check_authentication():
        return "Having issues logging in to ivoryOS, or ivoryOS server is not running."
    resp = client.get(f"{url}/edit_workflow/{workflow_name}")
    if resp.status_code == httpx.codes.OK:
        script = client.get(f"{url}/api/get_script").json()
        return script
    return "cannot get workflow script"

@mcp.tool("submit_workflow_script")
def submit_workflow_script(main_script: str = "", cleanup_script: str = "", prep_script: str = "") -> str:
    """get current workflow script"""
    if not _check_authentication():
        return "Having issues logging in to ivoryOS, or ivoryOS server is not running."
    client.post(f"{url}/api/get_script", data={"script": main_script, "cleanup": cleanup_script, "prep": prep_script})
    return "Updated"

@mcp.tool("get_workflow_execution_status")
def get_workflow_execution_status():
    """get workflow status"""
    if not _check_authentication():
        return "Having issues logging in to ivoryOS, or ivoryOS server is not running."
    msg = client.get(f"{url}/api/status").json()
    return msg

if __name__ == "__main__":
    print("Running...")