# Day 10 – MCP & Function Calling

_Timebox: ~1 hour_

## Knowledge goals

- Understand the **Model Context Protocol (MCP)** and how it relates to Function Calling  
- Define the core architecture, roles, and purpose of MCP  
- Compare Function Calling vs MCP with concrete examples  
- Learn best practices for choosing the right approach in AI systems  

## Learning materials (≈ 20–25 minutes)

- Read: **Function Calling vs. Model Context Protocol (MCP)**  
  Comparative explanations and visuals on how LLMs decide actions (Function Calling) vs how tools are standardized and invoked (MCP).  
  Reference: Akshay Pachaar (LinkedIn)

- Read: **Model Context Protocol (MCP) – Introduction & Architecture**  
  Official MCP documentation explaining client–server architecture, discovery, and standardization.  
  Reference: modelcontextprotocol.io

- Read: **Function Calling vs MCP in Production Systems**  
  Enterprise-focused discussion on scalability, reuse, and operational trade-offs.  
  Reference: FotieCodes / Medium articles

## Core concepts

### What is Function Calling?

- A **model capability** where an LLM emits a structured request to invoke a specific function or tool.  
- Developers define:
  - Function name  
  - Input schema  
  - Output expectations  
- The LLM selects *which* function to call and *with what arguments*.  
- Execution logic is usually tightly coupled to application code.  
- Best suited for:
  - Small systems  
  - Prototypes  
  - Direct, well-defined tool usage  

### What is MCP (Model Context Protocol)?

- MCP is an **open protocol** that standardizes how AI applications interact with external tools and services.  
- Introduces a **client–server abstraction**:
  - MCP Client: used by the AI application
  - MCP Server: exposes tools in a standardized way
- Key capabilities:
  - Tool discovery
  - Standardized schemas
  - Decoupled execution
  - Transport abstraction (e.g., STDIO, HTTP)
- Designed for:
  - Large agent systems
  - Multi-tool environments
  - Cross-model and cross-app reuse

## How they fit together

- **Function Calling** answers: *What does the model want to do?*  
- **MCP** answers: *How are tools discovered, executed, and managed at scale?*  

In practice:
- Function calling often produces the **intent**
- MCP provides the **runtime and infrastructure** to fulfill that intent

## Activities (≈ 30–40 minutes)

### Step 1: Key terms (5–8 minutes)

- **Tool Schema** – Structured definition of tool inputs and outputs  
- **MCP Client** – Interface used by the AI application to communicate with MCP  
- **MCP Server** – Service exposing tools through MCP  
- **Transport** – Communication layer (STDIO, HTTP)

### Step 2: MCP architecture overview (10–12 minutes)

1. User prompt enters the host application (agent / IDE / UI)
2. MCP Client prepares a standardized request
3. MCP Server discovers available tools
4. Tool execution happens inside the server
5. Results are returned to the client and then to the LLM

### Step 3: Example comparison (10–15 minutes)

#### Function Calling

```json
{
  "name": "get_weather",
  "arguments": {
    "location": "Paris",
    "units": "metric"
  }
}
```

#### MCP-based approach

- Intent expressed by the model
- MCP Client routes the request
- MCP Server selects and executes the tool
- Standardized result returned to the model

### Step 4: Pros & cons

| Dimension | Function Calling | MCP |
|---------|------------------|-----|
| Setup complexity | Low | Medium |
| Scalability | Limited | High |
| Tool reuse | Low | High |
| Best use case | MVPs | Production systems |

## Knowledge check

- What problem does MCP solve beyond function calling?
- When is direct function calling sufficient?
- When does MCP become necessary?

## Next steps

- Implement a minimal MCP server
- Connect multiple tools via MCP
- Compare with a function-calling-only approach
