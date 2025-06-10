# IvoryOS MCP server

![](https://badge.mcpx.dev?type=server 'MCP Server')
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### General tools
*[x] `platform-info`: get the signature of the current platform.
*[x] `execution-status` get if the system is busy and the current/last task status

### Direct control
*[x] `execute-task` Backend function call

### Workflow design
Tools:
*[x] `load-workflow-script`: get a workflow script by name from database
*[ ] `submit-workflow-script`: save a workflow Python script to database
*[ ] `create-execution-plan`: 

Prompt:
*[x] `generate-workflow-script`


### Workflow control
*[x] `pause-and-resume`
*[x] `abort-pending-workflow-iterations`
*[x] `stop-current-workflow`


### Workflow data
*[ ]  List available workflow data
*[ ]  Load data csv and execution detail from selected workflow
