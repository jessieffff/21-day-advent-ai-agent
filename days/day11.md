# Day 11 – Agent Skills, Function Calling & MCP

_Timebox: ~1 hour_

## Knowledge goals

- Understand what **Agent Skills** are and why they were introduced  
- Learn how **Agent Skills** differ from **Function Calling** and **MCP (Model Context Protocol)**  
- Understand how these three concepts fit together in real agent systems  
- Develop intuition for choosing the right abstraction in different scenarios  

## Learning materials (≈ 20–25 minutes)

- Read: **About Agent Skills**  
  Official explanation of what Agent Skills are, how they work, and when to use them.  
  Reference: GitHub Docs — About Agent Skills  
  https://docs.github.com/copilot/concepts/agents/about-agent-skills

- Read: **Use Agent Skills in VS Code**  
  Practical guide to skill structure, discovery, and usage in Copilot agent mode.  
  Reference: VS Code Docs — Agent Skills  
  https://code.visualstudio.com/docs/copilot/customization/agent-skills

- Read: **Enhancing GitHub Copilot agent mode with MCP**  
  How MCP is used to expose tools and capabilities to Copilot agents.  
  Reference: GitHub Docs — MCP and Agent Mode  
  https://docs.github.com/en/copilot/tutorials/enhance-agent-mode-with-mcp

- Read: **Model Context Protocol (MCP) – Overview**  
  High-level explanation of MCP as an open protocol for tool and data integration.  
  Reference: Model Context Protocol  
  https://modelcontextprotocol.io

## Core concepts

### What are Agent Skills?

- Agent Skills are reusable, repository-scoped bundles of instructions, examples, scripts, and supporting resources.
- They teach Copilot how to perform a multi-step workflow, not just how to answer a question.
- Skills are loaded on demand when Copilot determines they are relevant to the user’s request.
- A skill encodes when it should be used, how a task should be carried out, and what outputs are expected.

### What is Function Calling?

- Function Calling is a model capability where an LLM emits a structured request to invoke a specific function.
- Developers define function names, input schemas, and output expectations.
- The model decides which function to call and with what arguments.
- Best suited for single, well-defined actions.

### What is MCP (Model Context Protocol)?

- MCP is an open protocol that standardizes how AI applications interact with external tools and data sources.
- It introduces a client–server architecture with MCP Clients and MCP Servers.
- Designed for scalable, multi-tool, cross-application agent systems.

## How they fit together

- Function Calling answers what action to take.
- MCP defines how tools are discovered and executed.
- Agent Skills define how a full workflow should be performed end to end.

## Pros & cons

Function Calling: simple, low setup, limited scalability.  
MCP: scalable, reusable tool infrastructure.  
Agent Skills: high-level, repeatable workflows.

## Activities

- Define when you would use each abstraction.
- Map them onto an agent workflow you are building.

## Knowledge check

- What problem do Agent Skills solve beyond function calling?
- When does MCP become necessary?
- How do these three concepts complement each other?
