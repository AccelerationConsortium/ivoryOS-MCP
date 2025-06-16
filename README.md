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
Option 1: in `.env`, change ivoryOS url and login credentials. 
```
IVORYOS_URL=http://127.0.0.1:8000/ivoryos
IVORYOS_USERNAME=admin
IVORYOS_PASSWORD=admin
```


Option 2: In `ivoryos_mcp/server.py`, change ivoryOS url and login credentials. 
```python
url = "http://127.0.0.1:8000/ivoryos"
login_data = {
    "username": "admin",
    "password": "admin",
}
```

## 🚀 Install the server (in [Claude Desktop](https://claude.ai/download))
```bash
mcp install ivoryos_mcp/server.py
```

## ✨ Features
| **Category**            | **Feature**              | **Description**                                        |
|-------------------------|--------------------------|--------------------------------------------------------|
| **ℹ️ General Tools**    | `platform-info`          | Get ivoryOS info and signature of the platform         |
|                         | `execution-status`       | Check if system is busy and current/last task status   |
| **ℹ️ Workflow Design**  | `list-workflow-scripts`  | List all workflow scripts from the database            |
|                         | `load-workflow-script`   | Load a workflow script from the database               |
|                         | `submit-workflow-script` | Save a workflow Python script to the database          |
| **ℹ️ Workflow Data**    | `list-workflow-data`     | List available workflow execution data                 |
|                         | `load-workflow-data`     | Load CSV and execution log from selected workflow      |
| **🤖 Direct Control**   | `execute-task`           | Call platform function directly                        |
| **🤖 Workflow Run**     | `run-workflow-repeat`    | Run workflow scripts repeatedly with static parameters |
|                         | `run-workflow-kwargs`    | Run workflow scripts with dynamic parameters           |
|                         | `run-workflow-campaign`  | Run workflow campaign with an optimizer                |
| **🤖 Workflow Control** | `pause-and-resume`       | Pause or resume the workflow execution                 |
|                         | `abort-pending-workflow` | Finish current iteration, abort future executions      |
|                         | `stop-current-workflow`  | Safe stop of current workflow                          |

> ⚠️ It's recommended to only use **`allow always`** for tasks with ℹ️ 
> and use **`allow once`** for tasks with 🤖. 
> These tasks will trigger actual actions on your hosted Python code.


## 🧪 Examples
The example prompt uses the abstract SDL example.
### Platform info
![status.gif](https://gitlab.com/heingroup/ivoryos-suite/ivoryos-mcp/-/raw/main/docs/status.gif)

### Load prebuilt workflow script 
![load script.gif](https://gitlab.com/heingroup/ivoryos-suite/ivoryos-mcp/-/raw/main/docs/load%20script.gif)