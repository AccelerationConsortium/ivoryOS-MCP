# server.py
from typing import Optional

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
    try:
        resp = client.get(f"{url}/", follow_redirects=False)
        if resp.status_code == httpx.codes.OK:
            return True
        else:
            login_resp = client.post(f"{url}/login", data=login_data)
            return login_resp.status_code == 200
    except httpx.ConnectError:
        return False


@mcp.tool("platform-info")
def summarize_deck_function() -> str:
    """
    summarize the current deck functions
    """
    try:
        snapshot = client.get(f"{url}/backend_control").json()
        return (
            """
            IvoryOS is a unified task and workflow orchestrator.
            workflow execution has 3 blocks, prep, main (iterate) and cleanup.
            one can execute the workflow using 3 options
            1. simple repeat with `run-workflow-repeat`
            2. repeat with kwargs `run-workflow-kwargs`
            3. campaign `run-workflow-campaign`
            IvoryOS is a unified task and workflow orchestrator.
            workflow execution has 3 blocks, prep, main (iterate) and cleanup.
            one can execute the workflow using 3 options
            1. simple repeat with `run-workflow-repeat`
            2. repeat with kwargs `run-workflow-kwargs`
            3. campaign `run-workflow-campaign`, use `ax_campaign_design` to for campaign design
            """
            f"you can summarize the available python function representation {snapshot}")
    except Exception:
        return "there is not deck available."


@mcp.tool("execution-status")
def execution_status():
    """
    get workflow status
    :return:
    if not busy:   {'busy': False, 'last_task': {}}
    if busy:       {'busy': True, 'current_task': {'end_time': None, 'id': 7, 'kwargs': {'amount_in_mg': '5', 'bring_in': 'false'}, 'method_name': 'AbstractSDL.dose_solid', 'output': None, 'run_error': '0', 'start_time': 'Tue, 10 Jun 2025 13:41:27 GMT'}}
    """
    if not _check_authentication():
        return "Having issues logging in to ivoryOS, or ivoryOS server is not running."
    resp = client.get(f"{url}/api/status")
    if resp.status_code == httpx.codes.OK:
        return resp.json()
    else:
        return "cannot get workflow status"


@mcp.tool("execute-task")
def execute_task(component: str, method: str, kwargs: dict = None) -> str:
    """
    Execute a robot task and return task_id.

    :param component: deck component (e.g. sdl)
    :param method: method name (e.g. dose_solid)
    :param kwargs: method keyword arguments (e.g. {'amount_in_mg': '5'})
    :return: {'status': 'task started', 'task_id': 7}
    """
    if kwargs is None:
        kwargs = {}

    snapshot = client.get(f"{url}/backend_control").json()
    component = component if component.startswith("deck.") else f"deck.{component}"

    if component not in snapshot:
        return f"The component {component} does not exist in {snapshot}."

    kwargs["hidden_name"] = method
    # only submit the task without waiting for completion.
    kwargs["hidden_wait"] = False
    resp = client.post(f"{url}/backend_control/{component}", data=kwargs)
    if resp.status_code == httpx.codes.OK:
        result = resp.json()
        return f"{result}. Use `execution-status` to monitor."
    else:
        return "there is not deck available."

@mcp.tool("list-workflow-scripts")
def list_workflow_script(search_key:str='', deck_name:str='') -> str:
    """get current workflow script"""
    if not _check_authentication():
        return "Having issues logging in to ivoryOS, or ivoryOS server is not running."
    resp = client.get(f"{url}/database/{deck_name}", params={"keyword": search_key})
    if resp.status_code == httpx.codes.OK:
        return resp.json()
    return "cannot get workflow script"


@mcp.tool("load-workflow-script")
def load_workflow_script(workflow_name: str) -> str:
    """get current workflow script"""
    if not _check_authentication():
        return "Having issues logging in to ivoryOS, or ivoryOS server is not running."
    resp = client.get(f"{url}/edit_workflow/{workflow_name}")
    if resp.status_code == httpx.codes.OK:
        script = client.get(f"{url}/api/get_script").json()
        return script
    return "cannot get workflow script"


@mcp.tool("submit-workflow-script")
def submit_workflow_script(workflow_name: str, main_script: str = "", cleanup_script: str = "", prep_script: str = "") -> str:
    """get current workflow script"""
    if not _check_authentication():
        return "Having issues logging in to ivoryOS, or ivoryOS server is not running."
    response = client.post(f"{url}/api/get_script", json={"workflow_name":workflow_name, "script": main_script, "cleanup": cleanup_script, "prep": prep_script})
    if response.status_code == httpx.codes.OK:
        return "Updated"
    return "cannot update workflow script"


@mcp.prompt("generate-workflow-script")
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


@mcp.prompt("campaign-design")
def ax_campaign_design() -> str:
    """summarize the current deck functions"""
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



# ------------------------------
# --- workflow control tools ---
# ------------------------------
@mcp.tool("pause-and-resume")
def pause_and_resume() -> str:
    """toggle pause and resume for workflow execution"""
    if not _check_authentication():
        return f"Having issues logging in to ivoryOS."
    msg = client.post(f"{url}/api/pause").json()
    return msg


@mcp.tool("abort-pending-workflow")
def abort_pending_workflow_iterations() -> str:
    """abort pending workflow execution"""
    if not _check_authentication():
        return f"Having issues logging in to ivoryOS, or ivoryOS server is not running."
    msg = client.post(f"{url}/api/abort_pending").json()
    return msg


@mcp.tool("stop-current-workflow")
def stop_workflow() -> str:
    """stop workflow execution after current step"""
    if not _check_authentication():
        return f"Having issues logging in to ivoryOS, or ivoryOS server is not running."
    msg = client.post(f"{url}/api/abort_current").json()
    return msg


@mcp.tool("run-workflow-repeat")
def run_workflow(repeat_time: Optional[int] = None) -> str:
    """
    run the loaded workflow with repeat times
    :param repeat_time:
    :return:
    """
    if not _check_authentication():
        return f"Having issues logging in to ivoryOS, or ivoryOS server is not running."
    response = client.post(f"{url}/experiment", data={"repeat": str(repeat_time)})
    if response.status_code == httpx.codes.OK:
        return response.json()
    return "cannot get workflow data"


@mcp.tool("run-workflow-kwargs")
def run_workflow_with_kwargs(kwargs_list: list[dict] = None) -> str | int:
    """
    run the loaded workflow with a list of key word arguments (kwargs)
    :param kwargs_list: [{"arg1":1, "arg2":2}, {"arg1":1, "arg2":2}]
    :return:
    """
    if not _check_authentication():
        return f"Having issues logging in to ivoryOS, or ivoryOS server is not running."
    response = client.post(f"{url}/experiment", json={"kwargs": kwargs_list})
    if response.status_code == httpx.codes.OK:
        return response.json()
    return "cannot get workflow data"


@mcp.tool("run-workflow-campaign")
def run_workflow_campaign(parameters: list[dict], objectives: list[dict], repeat: int = 25,
                          parameter_constraints: list[str] = []) -> str:
    """
    run the loaded workflow with ax-platform (credit: Honegumi)
    :param parameters: [
        {"name": "x1", "type": "range", "value": 10.0},
        {"name": "x2", "type": "fixed", "bounds": [0.0, 10.0]},
        {
            "name": "c1",
            "type": "choice",
            "is_ordered": False,
            "values": ["A", "B", "C"],
        },
    ]
    :param objectives: [
        {"name": "obj_1", "minimize": True},
        {"name": "obj_2", "minimize": False},
    ]
    :param repeat:
    :param parameter_constraints: [
        "x1 + x2 <= 15.0",
        "x1 + x2 <= {total}",
        "x1 <= x2",
        "1.0*x1 + 0.5*x2 <= 15.0",
    ],
    :return:
    """
    if not _check_authentication():
        return f"Having issues logging in to ivoryOS, or ivoryOS server is not running."
    response = client.post(f"{url}/experiment",
                           json={"parameters":parameters,
                                 "objectives":objectives,
                                 "parameter_constraints":parameter_constraints,
                                 "repeat": repeat,
                                 })
    if response.status_code == httpx.codes.OK:
        return response.json()
    return "cannot get workflow data"


@mcp.tool("list-workflow-data")
def list_workflow_data(workflow_name: str = "") -> str:
    """
    list workflow data
    :param workflow_name: load data that was acquired using `workflow name`
    :return: {'workflow_data': {'1': {'start_time': 'Mon, 09 Jun 2025 16:01:03 GMT', 'workflow_name': 'test1'}}}
    """
    if not _check_authentication():
        return "Having issues logging in to ivoryOS, or ivoryOS server is not running."
    resp = client.get(f"{url}/workflow_runs", params={"keyword": workflow_name})
    if resp.status_code == httpx.codes.OK:
        return resp.json()
    return "cannot get workflow data"


@mcp.tool("load-workflow-data")
def load_workflow_data(workflow_id: int) -> str:
    """
    list workflow data
    :param workflow_id: load data that was acquired using `workflow name`
    :return: {'workflow_data': {'1': {'start_time': 'Mon, 09 Jun 2025 16:01:03 GMT', 'workflow_name': 'test1'}}}
    """
    if not _check_authentication():
        return "Having issues logging in to ivoryOS, or ivoryOS server is not running."
    resp = client.get(f"{url}/workflow_steps/{workflow_id}")
    if resp.status_code == httpx.codes.OK:
        return resp.json()
    return "cannot get workflow data"


if __name__ == "__main__":
    print("Running...")
