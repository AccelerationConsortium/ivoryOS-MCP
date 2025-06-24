# server.py
import os
from typing import Optional

from mcp.server.fastmcp import FastMCP
import httpx
from dotenv import load_dotenv
# Create an MCP server
mcp = FastMCP("IvoryOS MCP")

load_dotenv()
url = os.getenv("IVORYOS_URL", "http://127.0.0.1:8000/ivoryos")
login_data = {
    "username": os.getenv("IVORYOS_USERNAME", "admin"),
    "password": os.getenv("IVORYOS_PASSWORD", "admin"),
}
ivoryos_client = httpx.Client(follow_redirects=True)

def main():
    mcp.run()


def _check_authentication():
    try:
        resp = ivoryos_client.get(f"{url}/", follow_redirects=False)
        if resp.status_code == httpx.codes.OK:
            return
        login_resp = ivoryos_client.post(f"{url}/auth/login", data=login_data)
        if login_resp.status_code != 200:
            raise RuntimeError(f"Login failed")
    except httpx.ConnectError as e:
        raise ConnectionError(f"Connection error during authentication: {e}") from e


@mcp.tool("platform-info")
def summarize_deck_function() -> str:
    """
    summarize ivoryOS and the current deck functions, no authentication required.
    """
    try:
        snapshot = ivoryos_client.get(f"{url}/api/control").json()
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
    if busy:       {'busy': True,
                    'current_task': {
                        'end_time': None,
                        'id': 7,
                        'kwargs': {'amount_in_mg': '5', 'bring_in': 'false'},
                        'method_name': 'AbstractSDL.dose_solid',
                        'output': None,
                        'run_error': '0',
                        'start_time': 'Tue, 10 Jun 2025 13:41:27 GMT'
                    }
                    }
    """
    try:
        _check_authentication()
        resp = ivoryos_client.get(f"{url}/api/runner/status")
        if resp.status_code == httpx.codes.OK:
            return resp.json()
        else:
            return f"Error getting workflow status {resp.status_code}"
    except Exception as e:
        return f"Error getting workflow status {str(e)}"


@mcp.tool("execute-task")
def execute_task(component: str, method: str, kwargs: dict = None) -> str:
    """
    Execute a robot task and return task_id.

    :param component: deck component (e.g. sdl)
    :param method: method name (e.g. dose_solid)
    :param kwargs: method keyword arguments (e.g. {'amount_in_mg': '5'})
    :return: {'status': 'task started', 'task_id': 7}
    """
    try:
        _check_authentication()
        if kwargs is None:
            kwargs = {}

        snapshot = ivoryos_client.get(f"{url}/api/control").json()
        component = component if component.startswith("deck.") else f"deck.{component}"

        if component not in snapshot:
            return f"The component {component} does not exist in {snapshot}."

        kwargs["hidden_name"] = method

        # only submit the task without waiting for completion.
        kwargs["hidden_wait"] = False
        resp = ivoryos_client.post(f"{url}/api/control/{component}", data=kwargs)
        if resp.status_code == httpx.codes.OK:
            result = resp.json()
            return f"{result}. Use `execution-status` to monitor."
        else:
            return f"Error submitting tasks {resp.status_code}"
    except Exception as e:
        return f"Error submitting tasks {str(e)}"

@mcp.tool("list-workflow-scripts")
def list_workflow_script(search_key:str='', deck_name:str='') -> str:
    """
    get current workflow script
    :param search_key: workflow name search key
    :param deck_name: deck name
    :return: list of workflow scripts
    """
    try:
        _check_authentication()
        resp = ivoryos_client.get(f"{url}/database/scripts/{deck_name}", params={"keyword": search_key})
        if resp.status_code == httpx.codes.OK:
            return resp.json()
        else:
            return f"Error listing workflow script: {resp.status_code}"
    except Exception as e:
        return f"Error listing workflow script: {str(e)}"


@mcp.tool("load-workflow-script")
def load_workflow_script(workflow_name: str) -> str:
    """
    get current workflow script
    :param workflow_name: workflow name
    :return: compiled Python script of the workflow script
    """
    try:
        _check_authentication()
        resp = ivoryos_client.get(f"{url}/database/scripts/edit/{workflow_name}")
        if resp.status_code == httpx.codes.OK:
            script = resp.json()
            return script
        else:
            return f"Error loading workflow script: {resp.status_code}"
    except Exception as e:
        return f"Error loading workflow script: {str(e)}"


@mcp.tool("submit-workflow-script")
def submit_workflow_script(workflow_name: str, main_script: str = "", cleanup_script: str = "", prep_script: str = "") -> str:
    """get current workflow script"""
    try:
        _check_authentication()
        resp = ivoryos_client.post(url=f"{url}/api/design/submit",
                                   json={
                               "workflow_name":workflow_name,
                               "script": main_script,
                               "cleanup": cleanup_script,
                               "prep": prep_script
                           })
        if resp.status_code == httpx.codes.OK:
            return "Updated"
        else:
            return f"Error submitting workflow script: {resp.status_code}"
    except Exception as e:
        return f"Error submitting workflow script: {str(e)}"


@mcp.prompt("generate-workflow-script")
def generate_custom_script() -> str:
    """prompt for writing workflow script. no authentication required"""
    try:
        snapshot = httpx.get(f"{url}/api/control").json()
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
    """prompt for writing workflow campaign. no authentication required (template credit: Honegumi)"""
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
    try:
        _check_authentication()
        resp = ivoryos_client.post(f"{url}/api/runner/pause")
        if resp.status_code == httpx.codes.OK:
            return resp.json()
        else:
            return f"Error toggling workflow pause/resume: {resp.status_code}"
    except Exception as e:
        return f"Error toggling workflow pause/resume: {str(e)}"


@mcp.tool("abort-pending-workflow")
def abort_pending_workflow_iterations() -> str:
    """abort pending workflow execution"""
    try:
        _check_authentication()
        resp = ivoryos_client.post(f"{url}/api/runner/abort_pending")
        if resp.status_code == httpx.codes.OK:
            return resp.json()
        else:
            return f"Error aborting pending workflow: {resp.status_code}"
    except Exception as e:
        return f"Error aborting pending workflow: {str(e)}"


@mcp.tool("stop-current-workflow")
def stop_workflow() -> str:
    """stop workflow execution after current step"""
    try:
        _check_authentication()
        resp = ivoryos_client.post(f"{url}/api/runner/abort_current")
        if resp.status_code == httpx.codes.OK:
            return resp.json()
        else:
            return f"Error aborting current workflow: {resp.status_code}"
    except Exception as e:
        return f"Error aborting current workflow: {str(e)}"


@mcp.tool("run-workflow-repeat")
def run_workflow(repeat_time: Optional[int] = None) -> str:
    """
    run the loaded workflow with repeat times
    :param repeat_time:
    :return:
    """
    try:
        _check_authentication()
        resp = ivoryos_client.post(f"{url}/design/campaign", json={"repeat": str(repeat_time)})
        if resp.status_code == httpx.codes.OK:
            return resp.json()
        else:
            return f"Error starting workflow execution: {resp.status_code}"
    except Exception as e:
        return f"Error starting workflow execution: {str(e)}"


@mcp.tool("run-workflow-kwargs")
def run_workflow_with_kwargs(kwargs_list: list[dict] = None) -> str | int:
    """
    run the loaded workflow with a list of key word arguments (kwargs)
    :param kwargs_list: [{"arg1":1, "arg2":2}, {"arg1":1, "arg2":2}]
    :return:
    """
    try:
        _check_authentication()
        resp = ivoryos_client.post(f"{url}/design/campaign", json={"kwargs": kwargs_list})
        if resp.status_code == httpx.codes.OK:
            return resp.json()
        else:
            return f"Error starting workflow execution: {resp.status_code}"
    except Exception as e:
        return f"Error starting workflow execution: {str(e)}"


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
    try:
        _check_authentication()
        resp = ivoryos_client.post(f"{url}/design/campaign",
                                   json={"parameters":parameters,
                                     "objectives":objectives,
                                     "parameter_constraints":parameter_constraints,
                                     "repeat": repeat,
                                     })
        if resp.status_code == httpx.codes.OK:
            return resp.json()
        else:
            return f"Error starting workflow execution: {resp.status_code}"
    except Exception as e:
        return f"Error starting workflow execution: {str(e)}"


@mcp.tool("list-workflow-data")
def list_workflow_data(workflow_name: str = "") -> str:
    """
    list workflow data
    :param workflow_name: load data that was acquired using `workflow name`
    :return: {'workflow_data': {'1': {'start_time': 'Mon, 09 Jun 2025 16:01:03 GMT', 'workflow_name': 'test1'}}}
    """
    try:
        _check_authentication()
        resp = ivoryos_client.get(f"{url}/database/workflows/", params={"keyword": workflow_name})
        if resp.status_code == httpx.codes.OK:
            return resp.json()
        else:
            return f"Error listing workflow data: {resp.status_code}"
    except Exception as e:
        return f"Error listing workflow data: {str(e)}"


@mcp.tool("load-workflow-data")
def load_workflow_data(workflow_id: int) -> str:
    """
    list workflow data
    :param workflow_id: load data that was acquired using `workflow name`
    :return: {'workflow_data': {'1': {'start_time': 'Mon, 09 Jun 2025 16:01:03 GMT', 'workflow_name': 'test1'}}}
    """
    try:
        _check_authentication()
        resp = ivoryos_client.get(f"{url}/database/workflows/{workflow_id}")
        if resp.status_code == httpx.codes.OK:
            return resp.json()
        else:
            return f"Error listing workflow data: {resp.status_code}"
    except Exception as e:
        return f"Error listing workflow data: {str(e)}"

if __name__ == "__main__":
    print("Running...")
