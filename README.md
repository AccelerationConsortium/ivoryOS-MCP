# IvoryOS MCP server

![](https://badge.mcpx.dev?type=server 'MCP Server')
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Serve as a robot control interface using Model Context Protocol (MCP) to design, manage workflows, and interact with the current hardware/software execution layer.

## Features
| **Category**         | **Feature**                         | **Description**                                      | **Status** |
|----------------------|-------------------------------------|------------------------------------------------------|------------|
| **General Tools**    | `platform-info`                     | Get signature of the current platform                | ✅          |
|                      | `execution-status`                  | Check if system is busy and current/last task status | ✅          |
| **Direct Control**   | `execute-task`                      | Call backend function directly                       | ✅          |
| **Workflow Design**  | `list-workflow-scripts`             | List all workflow scripts from the database          | ✅          |
|                      | `load-workflow-script`              | Load a workflow script from the database             | ✅          |
|                      | `submit-workflow-script`            | Save a workflow Python script to the database        | ✅          |
|                      | `create-execution-plan`             | Build an execution plan from prompt/visual/script    | ✅          |
| **Workflow Control** | `pause-and-resume`                  | Pause or resume the workflow execution               | ✅          |
|                      | `abort-pending-workflow-iterations` | Finish current iteration, abort future executions    | ✅          |
|                      | `stop-current-workflow`             | Safe stop of current workflow                        | ✅          |
| **Workflow Data**    | `list-workflow-data`                | List available workflow execution data               | ✅          |
|                      | `load-workflow-data`                | Load CSV and execution log from selected workflow    | ✅          |

