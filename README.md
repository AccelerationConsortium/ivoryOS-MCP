# IvoryOS MCP server

![](https://badge.mcpx.dev?type=server 'MCP Server')
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Serve as a robot control interface using [IvoryOS](https://gitlab.com/heingroup/ivoryos) and Model Context Protocol (MCP) to design, manage workflows, and interact with the current hardware/software execution layer.


## 📦 Installation
Install [uv](https://docs.astral.sh/uv/).
### 1. Clone the Repository

```bash
git clone https://gitlab.com/heingroup/ivoryos-mpc
cd ivoryos-mcp
```
### 2. Install dependencies
When using IDE (e.g. PyCharm), the `uv` environment might be configured, you can skip this section.
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r uv.lock
```
## ⚙️ Configuration
In `ivoryos_mcp/server.py`, change ivoryOS url and login credentials. 
```python
url = "http://127.0.0.1:8000/ivoryos"
login_data = {
    "username": "admin",
    "password": "admin"
}
```
## 🚀 Install the server (in [Claude Desktop](https://claude.ai/download))
```bash
mcp install ivoryos_mcp/server.py
```

## ✨ Features
| **Category**         | **Feature**              | **Description**                                        | **Status** |
|----------------------|--------------------------|--------------------------------------------------------|------------|
| **General Tools**    | `platform-info`          | Get signature of the current platform                  | ✅          |
|                      | `execution-status`       | Check if system is busy and current/last task status   | ✅          |
| **Direct Control**   | `execute-task`           | Call backend function directly                         | ✅          |
| **Workflow Design**  | `list-workflow-scripts`  | List all workflow scripts from the database            | ✅          |
|                      | `load-workflow-script`   | Load a workflow script from the database               | ✅          |
|                      | `submit-workflow-script` | Save a workflow Python script to the database          | ✅          |
| **Workflow Run**     | `run-workflow-repeat`    | Run workflow scripts repeatedly with static parameters | ✅          |
|                      | `run-workflow-kwargs`    | Run workflow scripts with dynamic parameters           | ✅          |
|                      | `run-workflow-campaign`  | Run workflow campaign with an optimizer                | ✅          |
| **Workflow Control** | `pause-and-resume`       | Pause or resume the workflow execution                 | ✅          |
|                      | `abort-pending-workflow` | Finish current iteration, abort future executions      | ✅          |
|                      | `stop-current-workflow`  | Safe stop of current workflow                          | ✅          |
| **Workflow Data**    | `list-workflow-data`     | List available workflow execution data                 | ✅          |
|                      | `load-workflow-data`     | Load CSV and execution log from selected workflow      | ✅          |

## 🧪 Examples